from datetime import datetime, timedelta

from django.db.models import Count, Q
from django.shortcuts import render
from django.views.generic.base import View

from dqe.models import IpadDetails, ApplyListDetail, Project
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu, Notice

# 查詢看板的數據，當前用戶所屬部門下的機台數量
# class DqeView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
#     template_name = 'dqe/echart_index.html'
from testManage.models import BugRegister, TaskArrange


class DqeView(LoginRequiredMixin, View):
    # def get(self, request):
    #     res = dict()
    #     # 传入所有部门名
    #     stobjs = list(Project.objects.values('pname'))
    #     project = []
    #     for i in stobjs:
    #         project.append(i['pname'])
    #     res['Project'] = project
    #
    #     filter = {}
    #     filter['fk_apply__applyState'] = 2
    #
    #     data = list(ApplyListDetail.objects.filter(**filter).values('platform', 'qty'))
    #
    #     da = list(Project.objects.values('pname'))
    #     count = 0
    #     ret = dict()
    #     for i in da:
    #         if data == []:
    #             ret[i['pname']] = 0
    #         else:
    #             # print(222)
    #             for j in data:
    #                 if j['platform'] == i['pname']:
    #                     count = count + int(j['qty'])
    #
    #                 ret[i['pname']] = count
    #             count = 0
    #     res['datas'] = ret
    #
    #     # 传入当前时间
    #     res['time'] = datetime.now()
    #
    #     menu = Menu.get_menu_by_request_url(url=self.request.path_info)
    #
    #     if menu is not None:
    #         res.update(menu)
    #
    #     return render(request, 'dqe/echart_index.html', res)
    def get(self, request):
        # 锁定当天日期,查找出当天的公布信息，如果数据库没有，则显示无
        now = datetime.now().date() + timedelta(days=1)
        # print(now)
        oldtime = now - timedelta(days=3)
        # print(oldtime)
        fields = ['id', 'tag', 'relDate', 'relContent', 'relUser', 'other', ]

        # django 查询时间段
        res = dict(
            datas=list(Notice.objects.filter(relDate__range=(oldtime, now)).values(*fields).order_by('-relDate')))

        # 显示Bug 测试员的排名
        count = BugRegister.objects.all().values('find_per').annotate(count=Count('find_per')).values('find_per',
                                                                                                      'count').order_by(
            '-count')
        res['count'] = count
        # 显示工程师 Bug 的排名
        sub_count = BugRegister.objects.all().values('sub_per').annotate(count=Count('sub_per')).values('sub_per',
                                                                                                        'count').order_by(
            '-count')

        res['sub_count'] = sub_count

        time = datetime.now().strftime('%Y-%m-%d')

        arrange = list(
            TaskArrange.objects.filter(tester=request.user, task_date__pub_date=str(time)).values(
                'comments').distinct())
        print(arrange)
        res['arrange'] = arrange

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)

        return render(request, 'system/system_index.html', res)
