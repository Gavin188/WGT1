import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import View

from overtime.forms import TimeTypeCreateForm
from overtime.models import TimeType
from system.mixin import LoginRequiredMixin
from system.models import Menu


# 產品類型 界面
class ProductTypeView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=TimeType.objects.all())

        # 專案
        prodtypes = TimeType.objects.all()
        res['prodtypes'] = prodtypes
        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)
        return render(request, 'system/ProductType/ProductType_List.html', res)


# 產品類型 详情列表
class ProductTypeListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'tname', 'tnumber', 'tscale', 'tdate', 'time_control']
        searchFields = ['ptname', ]  # 与数据库字段一致
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        res = dict(data=list(TimeType.objects.filter(**filters).values(*fields)))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 產品類型 新增 和 修改
class ProductTypeUpdateView(LoginRequiredMixin, View):
    # 注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):
        res = dict()
        # 加班管控
        time_list = []
        for time_con in TimeType.TIME_TYPE:
            time_dict = dict(key=time_con[0], value=time_con[1])
            time_list.append(time_dict)
        if 'id' in request.GET and request.GET['id']:
            prodtype = get_object_or_404(TimeType, pk=request.GET.get('id'))
            res['prodtype'] = prodtype
        else:

            prodtypes = TimeType.objects.all()
            res['prodtypes'] = prodtypes
        res['time'] = time_list
        return render(request, 'system/ProductType/ProductType_Update.html', res)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:  # id的存在，就是为了说明是新增数据还是编辑数据
            notice = get_object_or_404(TimeType, pk=request.POST.get('id'))
        else:
            notice = TimeType()

        notice_create_form = TimeTypeCreateForm(request.POST, instance=notice)
        if notice_create_form.is_valid():
            notice_create_form.save()
            notice.relUser = request.user.username
            notice.save()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 產品類型 删除
class ProductTypeDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            TimeType.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')
