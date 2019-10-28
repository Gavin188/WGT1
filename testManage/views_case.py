# Create your views here.
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from system.mixin import LoginRequiredMixin


#  案例管理
class CasemanageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'testManage/CaseManage.html')


#  案例管理列表
class CasemanageListView(LoginRequiredMixin, View):
    def post(self, request):
        res = {"success": "",
               "totalRows": "",
               "curPage": "",
               "data": " ", }

        data = [{
            'id': '1.1.1',
            'function': 'photos',
            'dri': '郭志航',
            'test_iro': '摄像头',

        }, {

            'id': '1.1.2',
            'function': 'camera',
            'dri': '余帅',
            'test_iro': '照相机',

        }, {

            'id': '1.1.3',
            'function': 'house',
            'dri': '郭文娜',
            'test_iro': '后盖',

        }]
        res['data'] = data
        res['success'] = True
        res['curPage'] = 1
        res['totalRows'] = 10
        print(res)
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class CaseFunFindView(LoginRequiredMixin, View):
    '''案例管理 - 显示测试项的具体测试功能'''

    def get(self, request):
        id = request.GET.get('id')
        print(id)
        context = {
            'id': id
        }
        return render(request, 'testManage/Case_fun.html', context)

    def post(self, request):
        pass
