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
from dqe.forms import ProductTypeCreateForm
from dqe.models import ProductType, Stage
from system.mixin import LoginRequiredMixin
from system.models import Structure,Menu

#產品類型 界面
class ProductTypeView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=ProductType.objects.all())

        # 專案
        prodtypes = ProductType.objects.all()
        res['prodtypes'] = prodtypes

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)
        return render(request, 'system/ProductType/ProductType_List.html',res)

#產品類型 详情列表
class ProductTypeListView(LoginRequiredMixin, View):
    def get(self, request):

        fields = ['id', 'ptname']
        searchFields = ['ptname', ] #与数据库字段一致
        filters = {i + '__icontains': request.GET.get(i,'') for i in searchFields if request.GET.get(i, '') }  #此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        res = dict(data=list(ProductType.objects.filter(**filters).values(*fields)))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


#產品類型 新增 和 修改
class ProductTypeUpdateView(LoginRequiredMixin, View):
    #注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):
        res = dict()
        if 'id' in request.GET and request.GET['id']:
            prodtype = get_object_or_404(ProductType, pk=request.GET.get('id'))
            res['prodtype'] = prodtype
        else:
            prodtypes = ProductType.objects.all()
            res['prodtypes'] = prodtypes

        return render(request, 'system/ProductType/ProductType_Update.html', res)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:  #id的存在，就是为了说明是新增数据还是编辑数据
            prodtype = get_object_or_404(ProductType, pk=request.POST.get('id'))
        else:
            prodtype = ProductType()

        prodtype_create_form = ProductTypeCreateForm(request.POST, instance=prodtype)

        if prodtype_create_form.is_valid():
            prodtype_create_form.save()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')

#產品類型 删除
class ProductTypeDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            ProductType.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')





