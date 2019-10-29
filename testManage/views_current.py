import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views import View

from system.mixin import LoginRequiredMixin

#  今日测试
from testManage.models import TestFun


class CurrentTestView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'testManage/CurrentTest.html')


#   今日测试列表
class CurrentTestListView(LoginRequiredMixin, View):
    def post(self, request):
        res = {"success": "",
               "totalRows": "",
               "curPage": "",
               "data": " ", }

        data = list(TestFun.objects.all().values())
        res['data'] = data
        res['success'] = True
        res['curPage'] = 1
        res['totalRows'] = 10
        print(res)
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
