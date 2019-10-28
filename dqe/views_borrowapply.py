import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import View

from dqe.models import ApplyList, ApplyListDetail, OperateCacheTable, AccessTable
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu


# 借入申請界面
class BorrowApplyView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=ApplyList.objects.all())

        # 部門
        structures = Structure.objects.all()
        res['structures'] = structures

        # 申請單狀態
        applyState_list = []
        for applyState in ApplyList.APPLYSTATE_TYPE:
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
        fields = ['id', 'applyNum', 'applyName', 'applyUser', 'applyDate', 'applyUnit', 'applyState',
                  'lendRemark']
        searchFields = ['applyDate', 'applyUnit', 'applyUser', 'applyState']  # 与数据库字段一致
        # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   i not in ['', ] and request.GET.get(i, '')}

        # 不管根据什么条件来筛选，都要根据部门，把相应部门的数据传递过去
        if not request.GET.get('applyUnit'):
            filters['applyUnit'] = str(request.user.department)

        # 查询Apply所有结果
        # res = dict(data=list(Apply.objects.values(*fields)))

        res = dict(data=list(ApplyList.objects.filter(**filters).values(*fields).order_by('-applyDate')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 借入申請刪除   ==>  可以說刪除申請單
# 思路：两种方式
# 第一种：改变库存中的申请状态 > 再删除该申请单对应的applyDetial的信息 > 再删除该申请单信息，
# 第二种：先将该申请单中的申请详情的信息 存放到 操作缓存表OperateCacheTable 》改库存状态  》 删申请详情 》再删该申请单

class BorrowApplyDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)

        if 'id' in request.POST and request.POST['id']:
            id_list = list(map(int, request.POST.get('id').split(',')))
            # print(id_list)
            # 根据相应的ID 筛选出申请单的状态，
            aplystate = list(ApplyList.objects.filter(id__in=id_list).values('applyState').distinct())
            # 如果状态是已经签核，则无法删除
            data_list = [i['applyState'] for i in aplystate if i['applyState'] == '2']
            # print(data_list)
            # 判断是否存在。如果存在就提示错误
            if data_list:
                res['result'] = False
                res['message'] = '已经签核的申请单无法删除!'
            else:
                ApplyList.objects.filter(id__in=id_list).delete()
                res['result'] = True
            # print(res)

        return HttpResponse(json.dumps(res), content_type='application/json')


#  退还所有的机台
class BorrowApplyReturnView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dqe/LoanConfirm/ScanReturn.html', None)

    def post(self, request):
        res = dict(result=False)
        sns = request.POST.get('sns').split('\r\n')
        # apply_id = request.GET.get('id')

        data = list(OperateCacheTable.objects.filter(fk_applylistdetail__fk_apply__applyState=2).values_list(
            'fk_inventory__sn'))
        all_sns = []

        for i in range(len(data)):
            all_sns.append(data[i][0])

        invalidSn = []  # 无效的sn
        if request.user.department:
            for sn in sns:
                if sn in all_sns:
                    da = OperateCacheTable.objects.get(fk_inventory__sn=sn)

                    da.fk_inventory.units_status = 1
                    da.returnDate = datetime.datetime.now()
                    da.fk_inventory.save()
                    da.save()

                    data = list(
                        OperateCacheTable.objects.filter(fk_inventory__sn=sn).values('fk_applylistdetail__fk_apply_id'))
                    apply_id = data[0]['fk_applylistdetail__fk_apply_id']

                    status = OperateCacheTable.objects.filter(fk_applylistdetail__fk_apply_id=apply_id).values(
                        'fk_inventory__units_status').distinct()

                    flag = True

                    for i in status:
                        if int(i['fk_inventory__units_status']) == 2 or int(i['fk_inventory__units_status']) == 3:
                            flag = False
                            break

                    if flag:
                        state = ApplyList.objects.get(id=apply_id)
                        state.applyState = 3
                        state.save()

                else:
                    invalidSn.append(sn)
        # 如果没有出现以下3种情况 則為1   # 1 表成功  2 表部分成功

        if invalidSn:
            res['invalidSn'] = invalidSn
            res['result'] = 2
        else:
            res['invStateSN'] = '無'
            res['result'] = 1
        return HttpResponse(json.dumps(res), content_type='application/json')


class BorrowWGTReturnView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dqe/LoanConfirm/WgtReturn.html', None)

    def post(self, request):
        res = dict(result=False)
        sns = request.POST.get('sns').split('\r\n')

        data = list(AccessTable.objects.filter(fk_accesslistdetail__fk_apply__applyState=2).values_list(
            'fk_accessory__sn'))
        all_sns = []

        for i in range(len(data)):
            all_sns.append(data[i][0])
        invalidSn = []  # 无效的sn
        if request.user.department:
            for sn in sns:
                if sn in all_sns:
                    da = AccessTable.objects.filter(fk_accessory__sn=sn)
                    for da in da:
                        da.fk_accessory.status = 2
                        da.returnDate = datetime.datetime.now()
                        da.fk_accessory.save()
                        da.save()

                    data = list(
                        AccessTable.objects.filter(fk_accessory__sn=sn).values(
                            'fk_accesslistdetail__fk_apply_id'))
                    apply_id = data[0]['fk_accesslistdetail__fk_apply_id']

                    status = AccessTable.objects.filter(fk_accesslistdetail__fk_apply_id=apply_id).values(
                        'fk_accessory__status').distinct()

                    flag = True

                    for i in status:
                        if int(i['fk_accessory__status']) == 1:
                            flag = False
                            break

                    if flag:
                        da = ApplyList.objects.get(id=apply_id)
                        da.applyState = 3
                        da.save()


                else:
                    invalidSn.append(sn)
        if invalidSn:
            res['invalidSn'] = invalidSn
            res['result'] = 2
        else:
            res['invStateSN'] = '無'

            res['result'] = 1

        return HttpResponse(json.dumps(res), content_type='application/json')
