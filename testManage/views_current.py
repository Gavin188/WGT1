import datetime
import json

from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views import View

from system.mixin import LoginRequiredMixin
from testManage.models import TestFun, TaskArrange, CaseRegister


class CurrentTestView(LoginRequiredMixin, View):
    '''今日测试首页'''

    def get(self, request):
        user = request.user
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        errmsg = ''
        arrange = list(TaskArrange.objects.filter(tester=user, task_date__pub_date=str(time)).values('comments'))
        if arrange:
            comments = []
            for i in arrange:
                if i['comments'] not in comments:
                    comments.append(i['comments'])

            if len(comments) != 1:
                errmsg = '今日的测试项重复，请检查'

            comment = comments[0]
            print('***--', comment)
            try:
                case_id = list(CaseRegister.objects.filter(function=comment).values())[0]
            except Exception:
                errmsg = comment + '还没有上传案例管理,稍等'
                case_id = ''

            context = {
                'arrange': comment,
                'errmsg': errmsg,
                'case_id': case_id
            }

        else:
            context = {
                'arrange': '今日还没有上传测试任务',
                'errmsg': errmsg
            }
        return render(request, 'testManage/CurrentTest.html', context)


class CurrentTestListView(LoginRequiredMixin, View):
    '''今日测试首页 列表'''

    def post(self, request):
        res = {"success": "",
               "totalRows": "",
               "curPage": "",
               "data": " ", }
        # 获取今日 的测试项ID
        c_id = int(request.GET.get('id'))
        data = list(TestFun.objects.filter(fk_case__id=c_id).values())
        count = len(data)
        pageIndex = request.POST.get('curPage')
        pageSize = request.POST.get('pageSize')
        pageInator = Paginator(data, pageSize)
        contacts = pageInator.page(pageIndex)
        data_list = []  # 最终返回的结果集合
        for contact in contacts:
            data_list.append(contact)
        res['data'] = data_list
        res['success'] = True
        res['totalRows'] = count
        res['curPage'] = pageIndex
        # print(res)
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
