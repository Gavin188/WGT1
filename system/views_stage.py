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
from dqe.forms import StageCreateForm
from dqe.models import Stage, Stage, Project
from system.mixin import LoginRequiredMixin
from system.models import Structure,Menu

#专案界面
class StageView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=Stage.objects.all())

        # 專案
        projects = Project.objects.all()
        res['projects'] = projects

        # 階段
        stages = Stage.objects.all()
        res['stages'] = stages

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)
        return render(request, 'system/Stage/Stage_List.html',res)

#申请详情列表
class StageListView(LoginRequiredMixin, View):
    def get(self, request):

        fields = ['id','sname']
        searchFields = ['sname' ] #与数据库字段一致
        filters = {i + '__icontains': request.GET.get(i,'') for i in searchFields if request.GET.get(i, '') }  #此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        res = dict(data=list(Stage.objects.filter(**filters).values(*fields)))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


#專案 新增 和 修改
class StageUpdateView(LoginRequiredMixin, View):
    #注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):
        res = dict()
        if 'id' in request.GET and request.GET['id']:
            stage = get_object_or_404(Stage, pk=request.GET.get('id'))
            res['stage'] = stage
        else:
            stages = Stage.objects.all()
            res['stages'] = stages

        return render(request, 'system/Stage/Stage_Update.html', res)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:  #id的存在，就是为了说明是新增数据还是编辑数据
            stage = get_object_or_404(Stage, pk=request.POST.get('id'))
        else:
            stage = Stage()

        stage_create_form = StageCreateForm(request.POST, instance=stage)

        if stage_create_form.is_valid():
            stage_create_form.save()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')

#阶段删除
class StageDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            Stage.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# # 专案 和 阶段 联动
# class ProjectAndStageLinkageView(LoginRequiredMixin, View):
#
#     def post(self, request):
#
#         res = dict()
#
#         if request.POST.get('fk_project_id'):
#             stages = Stage.objects.filter(fk_project_id=request.POST.get('fk_project_id')).values(*['id','sname'])
#             res['stages'] = list(stages)
#
#         return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')