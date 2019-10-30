import datetime
import json

from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views import View

from system.mixin import LoginRequiredMixin
#  今日测试
from system.models import TestWord
from testManage.models import TestFun, TaskArrange, CaseRegister


class CurrentTestView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        errmsg = ''
        arrange = list(TaskArrange.objects.filter(tester=user, task_date__pub_date=str(time)).values('comments'))
        print(arrange)
        if arrange:
            comments = []
            for i in arrange:
                if i['comments'] not in comments:
                    comments.append(i['comments'])

            if len(comments) != 1:
                errmsg = '今日的测试项重复，请检查'

            comment = comments[0]
            case_id = list(CaseRegister.objects.filter(function=comment).values())[0]
            context = {
                'arrange': comment,
                'errmsg': errmsg,
                'case_id': case_id
            }
            print(comment)
            print(case_id)
        else:
            context = {
                'arrange': '今日还没有上传测试任务',
                'errmsg': errmsg
            }
        return render(request, 'testManage/CurrentTest.html', context)


#   今日测试列表
class CurrentTestListView(LoginRequiredMixin, View):
    def post(self, request):
        res = {"success": "",
               "totalRows": "",
               "curPage": "",
               "data": " ", }

        data = list(TestFun.objects.all().values())
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
