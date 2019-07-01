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
from dqe.forms import ApplyDetailCreateForm
from dqe.models import ApplyDetail, Project, Stage
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu


# 庫存界面
class ApplyDetailView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=ApplyDetail.objects.all())

        # 機台確認狀態
        machineState_list = []
        for machineState in ApplyDetail.MACHINE_STATE:
            machineState_dict = dict(key=machineState[0], value=machineState[1])
            machineState_list.append(machineState_dict)
        res['machineState_list'] = machineState_list

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)

        return render(request, 'dqe/ApplyDetail/ApplyDetail_List.html', res)


# 申请详情列表
class ApplyDetailListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'fk_apply', 'fk_inventory', 'machineState', 'fk_apply__applyNum', 'fk_inventory__rel',
                  'fk_apply__applyDate', 'lendDate']
        searchFields = ['fk_inventory__rel', 'machineState', ]  # 与数据库字段一致
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
        # print(filters)
        # 查询ApplyDetail所有结果
        # res = dict(data=list(ApplyDetail.objects.values(*fields)))
        filters['fk_apply'] = request.GET.get('applyId')

        res = dict(data=list(
            ApplyDetail.objects.filter(**filters).values(*fields).order_by('-fk_apply__applyDate',
                                                                           '-lendDate')))
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 申请详情 新增 和 修改
# get方式是跳转链接，而post方式是submit
class ApplyDetailUpdateView(LoginRequiredMixin, View):
    # 注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):
        res = dict()

        # 機台確認狀態
        machineState_list = []
        for machineState in ApplyDetail.MACHINE_STATE:
            machineState_dict = dict(key=machineState[0], value=machineState[1])
            machineState_list.append(machineState_dict)
        res['machineState_list'] = machineState_list

        if 'id' in request.GET and request.GET['id']:
            applydetail = get_object_or_404(ApplyDetail, pk=request.GET.get('id'))
            res['applydetail'] = applydetail
        else:
            applydetails = ApplyDetail.objects.all()
            res['applydetails'] = applydetails

        return render(request, 'dqe/ApplyDetail/ApplyDetail_Update.html', res)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:  # id的存在，就是为了说明是新增数据还是编辑数据
            applydetail = get_object_or_404(ApplyDetail, pk=request.POST.get('id'))
        else:
            applydetail = ApplyDetail()

        applydetail_create_form = ApplyDetailCreateForm(request.POST, instance=applydetail)

        if applydetail_create_form.is_valid():
            applydetail_create_form.save()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 库存删除
class ApplyDetailDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            ApplyDetail.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')
