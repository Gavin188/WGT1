import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import View

from dqe.forms import FusedCreateForm, AccessCreateForm
from dqe.models import Fused, AccessDetails
from system.mixin import LoginRequiredMixin
from system.models import Menu, Access


# 专案界面
class AccessView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=Fused.objects.all())

        # 專案
        access = Access.objects.all()
        res['access'] = access

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)
        return render(request, 'system/Access/Access_List.html', res)


# 申请详情列表
class AccessListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'access']
        searchFields = ['access', ]  # 与数据库字段一致
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        res = dict(data=list(Access.objects.filter(**filters).values(*fields)))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 產品類型 新增 和 修改
class AccessUpdateView(LoginRequiredMixin, View):
    # 注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):
        res = dict()
        if 'id' in request.GET and request.GET['id']:
            access = get_object_or_404(Access, pk=request.GET.get('id'))
            res['access'] = access
        else:
            access = Access.objects.all()
            res['access'] = access

        return render(request, 'system/Access/Access_Update.html', res)

    def post(self, request):
        res = dict(result=False)
        print(request.POST.get('id'))
        if 'id' in request.POST and request.POST['id']:  # id的存在，就是为了说明是新增数据还是编辑数据
            access = get_object_or_404(Access, pk=request.POST.get('id'))
        else:
            access = Access()
        access_create_form = AccessCreateForm(request.POST, instance=access)
        if access_create_form.is_valid():
            access_create_form.save()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 產品類型 删除
class AccessDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            Access.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')
