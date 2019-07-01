import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from custom import BreadcrumbMixin
from dqe.forms import ApplyCreateForm
from dqe.models import Apply, Project, Stage, ApplyDetail, OperateCacheTable, Inventory
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu


# 借入申請界面
class BorrowApplyView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=Apply.objects.all())

        # 部門
        structures = Structure.objects.all()
        res['structures'] = structures

        # 申請單狀態
        applyState_list = []
        for applyState in Apply.APPLYSTATE_TYPE:
            applyState_dict = dict(key=applyState[0], value=applyState[1])
            applyState_list.append(applyState_dict)
        res['applyState_list'] = applyState_list

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)

        return render(request, 'dqe/BorrowApply/BorrowApply_List.html', res)


# 借入申請列表
class BorrowApplyListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'applyNum', 'applyUser', 'applyDate', 'applyUnit', 'applyTime', 'applyState', 'lendRemark']
        searchFields = ['applyDate', 'applyUnit', 'applyUser', 'applyState']  # 与数据库字段一致
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   i not in ['', ] and request.GET.get(i,
                                                       '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        # 假如时间采用区间的方式，用如下方式进行处理  时间格式转化 datetime.datetime.strptime(request.GET.get('StartDate'), "%m/%d/%Y")
        # if request.GET.get('startapplyDate'):
        #     filters['applyDate__gte'] = request.GET.get('startapplyDate')
        # if request.GET.get('endapplyDate'):
        #     filters['applyDate__lte'] = request.GET.get('endapplyDate')

        # 不管根据什么条件来筛选，都要根据部门，把相应部门的数据传递过去
        if not request.GET.get('applyUnit'):
            filters['applyUnit'] = str(request.user.department)

        # 查询Apply所有结果
        # res = dict(data=list(Apply.objects.values(*fields)))

        res = dict(data=list(Apply.objects.filter(**filters).values(*fields).order_by('-applyDate')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 进入申請單詳情界面
class BorrowApplyDetailView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            apply = get_object_or_404(Apply, pk=request.GET.get('id'))

        ret['apply'] = apply

        return render(request, 'dqe/BorrowApply/BorrowApply_Detail.html', ret)


# 申请详情列表
class BorrowApplyDetailListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'fk_inventory__fk_project__pname', 'fk_inventory__fk_stage__sname', 'fk_inventory__rel',
                  'fk_inventory__sn', 'fk_apply__applyNum', 'fk_apply__applyUser', 'fk_apply__applyUnit',
                  'fk_apply__applyDate', 'machineState',
                  'lendUnit', 'confirmUser', 'lendDate', 'remark', 'macAppState']
        searchFields = ['fk_inventory__rel', 'machineState', ]
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        # 查询ApplyDetail所有结果
        # res = dict(data=list(ApplyDetail.objects.values(*fields)))

        # 通过隐含传递的applyId，反向查出applydetail中所有对应该applyId的信息
        filters['fk_apply_id'] = request.GET.get('applyId')

        res = dict(data=list(ApplyDetail.objects.filter(**filters).values(*fields).order_by('-fk_apply__applyDate')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 借入申請刪除   ==>  可以說刪除申請單
# 思路：两种方式
# 第一种：改变库存中的申请状态 > 再删除该申请单对应的applyDetial的信息 > 再删除该申请单信息，
# 第二种：先将该申请单中的申请详情的信息 存放到 操作缓存表OperateCacheTable 》改库存状态  》 删申请详情 》再删该申请单

class BorrowApplyDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        # 采用第二种方式
        try:

            if 'id' in request.POST and request.POST['id']:

                id = request.POST.get('id')
                # 查该单的信息
                applyObj = Apply.objects.get(id=id)

                # 查出该单下的所有机台信息
                adobjs = ApplyDetail.objects.filter(fk_apply=applyObj)

                if request.POST.get('retain', ''):
                    # 保留机台信息到操作缓存表
                    for adobj in adobjs:
                        OperateCacheTable.objects.get_or_create(
                            fk_inventory=adobj.fk_inventory,
                            fk_structure=Structure.objects.get(name=applyObj.applyUnit),
                            opeuser=applyObj.applyUser
                        )
                        # 改库存状态
                        adobj.fk_inventory.state = 2
                        adobj.fk_inventory.save()

                    # 删除申请详情，删除申请单
                    adobjs.delete()
                    applyObj.delete()

                    res['result'] = True

                if request.POST.get('full', ''):
                    # 删除申请详情，删除申请单
                    for adobj in adobjs:
                        # 改库存状态
                        adobj.fk_inventory.state = 2
                        adobj.fk_inventory.save()

                    adobjs.delete()
                    applyObj.delete()

                    res['result'] = True

            else:
                pass


        except:
            pass

        return HttpResponse(json.dumps(res), content_type='application/json')
