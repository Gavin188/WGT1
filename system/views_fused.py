import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import View

from dqe.forms import FusedCreateForm
from dqe.models import Fused
from system.mixin import LoginRequiredMixin
from system.models import Menu


# 专案界面
class FusedView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=Fused.objects.all())

        # 專案
        fuseds = Fused.objects.all()
        res['fuseds'] = fuseds

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)
        return render(request, 'system/Fused/Fused_List.html', res)


# 申请详情列表
class FusedListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'fname']
        searchFields = ['fname', ]  # 与数据库字段一致
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        res = dict(data=list(Fused.objects.filter(**filters).values(*fields)))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 產品類型 新增 和 修改
class FusedUpdateView(LoginRequiredMixin, View):
    # 注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):
        res = dict()
        if 'id' in request.GET and request.GET['id']:
            fused = get_object_or_404(Fused, pk=request.GET.get('id'))
            res['fused'] = fused
        else:
            fuseds = Fused.objects.all()
            res['fuseds'] = fuseds

        return render(request, 'system/Fused/Fused_Update.html', res)

    def post(self, request):
        res = dict(result=False)
        print(request.POST.get('id'))
        if 'id' in request.POST and request.POST['id']:  # id的存在，就是为了说明是新增数据还是编辑数据
            fused = get_object_or_404(Fused, pk=request.POST.get('id'))
        else:
            fused = Fused()
        print(request.POST)
        fused_create_form = FusedCreateForm(request.POST, instance=fused)
        print(fused_create_form)
        if fused_create_form.is_valid():
            print(111)
            fused_create_form.save()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 產品類型 删除
class FusedDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            Fused.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')
