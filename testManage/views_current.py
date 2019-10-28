import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views import View

from system.mixin import LoginRequiredMixin


#  今日测试
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

        data = [{
            'id': '1.1.1',
            'function': 'phontos',
            'oper_step': '先快而慢',
            'expect': 'bad',
            # 'radar_id': 'DLXWC018JYN3',
            # 'desc': '文件',
            # 'comments': '的尚方宝剑',

        }, {

            'id': '1.1.2',
            'function': 'camera',
            'oper_step': '由远至今',
            'expect': 'good',
            # 'radar_id': 'DLXWC018JYN2',
            # 'desc': '长相',
            # 'comments': '大帅府',

        }, {

            'id': '1.1.3',
            'function': 'axia',
            'oper_step': '重力',
            'expect': 'well',
            # 'radar_id': 'DLXWC018JYN1',
            # 'desc': '声音',
            # 'comments': '张三',

        }]
        res['data'] = data
        res['success'] = True
        res['curPage'] = 1
        res['totalRows'] = 10
        print(res)
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
