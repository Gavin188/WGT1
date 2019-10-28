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
from system.forms import NoticeCreateForm
from system.models import Notice
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu


# 专案界面
class NoticeView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=Notice.objects.all())

        # 專案
        notices = Notice.objects.all()
        res['notices'] = notices

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)
        return render(request, 'system/Notice/Notice_List.html', res)


# 申请详情列表
class NoticeListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'tag', 'relDate', 'relContent', 'relUser', 'other', ]
        searchFields = ['relDate', ]  # 与数据库字段一致
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        res = dict(data=list(Notice.objects.filter(**filters).values(*fields).order_by('-relDate')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 專案 新增 和 修改
class NoticeUpdateView(LoginRequiredMixin, View):
    # 注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):
        res = dict()
        # print('id=--=', request.GET.get('id'))
        if 'id' in request.GET and request.GET['id']:
            notice = get_object_or_404(Notice, pk=request.GET.get('id'))
            res['notice'] = notice
        else:
            notices = Notice.objects.all()
            res['notices'] = notices
        # print('res,', res)
        return render(request, 'system/Notice/Notice_Update.html', res)

    def post(self, request):
        res = dict(result=False)
        # print('id==', request.POST['id'])
        if 'id' in request.POST and request.POST['id']:  # id的存在，就是为了说明是新增数据还是编辑数据
            notice = get_object_or_404(Notice, pk=request.POST.get('id'))
        else:
            notice = Notice()

        notice_create_form = NoticeCreateForm(request.POST, instance=notice)

        if notice_create_form.is_valid():
            notice_create_form.save()
            notice.relUser = request.user.username
            notice.save()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 库存删除
class NoticeDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            Notice.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')
