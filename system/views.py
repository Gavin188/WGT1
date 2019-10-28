from django.http import HttpResponse

from custom import BreadcrumbMixin
from django.views.generic import TemplateView

from django.shortcuts import render
from django.views.generic.base import View
# from dqe.models import Inventory
from testManage.models import BugRegister
from .mixin import LoginRequiredMixin
from datetime import datetime
from django.db.models import Count, Q
from system.models import Structure, Menu, Notice
from datetime import timedelta


class SystemView(LoginRequiredMixin, View):  # BreadcrumbMixin, TemplateView

    template_name = 'system/system_index.html'

    def get(self, request):
        # res = dict()
        # # 锁定当天日期,查找出当天的公布信息，如果数据库没有，则显示无
        # now = datetime.now().date() + timedelta(days=1)
        # # print(now)
        # oldtime = now - timedelta(days=3)
        # # print(oldtime)
        # fields = ['id', 'tag', 'relDate', 'relContent', 'relUser', 'other', ]
        #
        # # django 查询时间段
        # res = dict(
        #     datas=list(Notice.objects.filter(relDate__range=(oldtime, now)).values(*fields).order_by('-relDate')))
        #
        # count = BugRegister.objects.all().values('find_per').annotate(count=Count('find_per')).values('find_per',
        #                                                                                               'count').order_by(
        #     '-count')
        # res['count'] = count
        #
        # sub_count = BugRegister.objects.all().values('sub_per').annotate(count=Count('sub_per')).values('sub_per',
        #                                                                                                 'count').order_by(
        #     '-count')
        #
        # res['sub_count'] = sub_count
        #
        # # print(count)
        # menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        # if menu is not None:
        #     res.update(menu)

        return render(request, 'index.html', None)
