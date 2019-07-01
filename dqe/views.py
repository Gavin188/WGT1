from django.db.models import Count, Q
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View

from dqe.models import Apply, Inventory
from system.mixin import LoginRequiredMixin
from custom import BreadcrumbMixin
from system.models import Structure, Menu
from datetime import datetime


# 查詢看板的數據，當前用戶所屬部門下的機台數量
# class DqeView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
#     template_name = 'dqe/echart_index.html'

class DqeView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict()
        # 传入所有部门名
        stobjs = Structure.objects.filter(type="department")
        res['structures'] = stobjs

        # 统计每个部门下，现在有多少台机台
        res['datas'] = list(
            Inventory.objects.filter(~Q(fk_structure__type="unit")).values('fk_structure__name').annotate(
                count=Count('fk_structure__name')).values('fk_structure__name', 'count'))

        # 传入当前时间
        res['time'] = datetime.now()

        # 循环判断哪个部门没有机台，将0加入进去
        tempSt = []
        for i in res['datas']:
            print(i)
            tempSt.append(i['fk_structure__name'])

        # 查出哪一个部门没有机台，然后将默认数据存入
        for stobj in stobjs:
            if stobj.name not in tempSt:
                res['datas'].append({'fk_structure__name': stobj.name, 'count': 0})

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)

        if menu is not None:
            res.update(menu)

        return render(request, 'dqe/echart_index.html', res)


class calendarView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'calendar.html', None)
