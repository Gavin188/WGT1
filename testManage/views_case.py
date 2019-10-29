# Create your views here.
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from system.mixin import LoginRequiredMixin

#  案例管理
from system.models import TestWord
from testManage.models import CaseRegister


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

        data = list(CaseRegister.objects.all().values())

        res['data'] = data
        res['success'] = True
        res['curPage'] = 1
        res['totalRows'] = 10

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class CaseFunFindView(LoginRequiredMixin, View):
    '''案例管理 - 显示测试项的具体测试功能'''

    def get(self, request):
        id = request.GET.get('id')
        print(id)
        case = list(CaseRegister.objects.filter(id=id).values())[0]
        print(list(CaseRegister.objects.filter(id=id).values()))
        context = {
            'case': case
        }
        return render(request, 'testManage/Case_fun.html', context)

    def post(self, request):
        pass


class CaseDescIroView(LoginRequiredMixin, View):
    '''案例管理 - 显示测试说明的测试文档'''

    def get(self, request):

        fields = ['id', 'title', 'publisher', 'comments', 'desc_pack']
        id = request.GET.get('id')
        print(request.GET)
        errmsg = ''
        try:
            title = list(CaseRegister.objects.filter(id=id).values('desc'))[0]['desc']
        except Exception:
            errmsg = '用例编号不存在'

        all_obj = list(TestWord.objects.filter(title=title).values(*fields))
        print(title)
        if len(all_obj) == 0:
            errmsg = '你还没有添加测试说明'
        context = {
            'all': all_obj,
            'errmsg': errmsg
        }

        return render(request, 'system/Test_Word/DetailWord.html', context)

    def post(self, request):
        pass


class CaseModelInsertView(LoginRequiredMixin, View):
    '''案例模块新增保存'''

    def post(self, request):
        res = dict(result=False)
        function = request.POST.get('function')
        dri = request.POST.get('dri')
        desc = request.POST.get('desc')

        # 判断 数据是否完整
        if not all([function, dri, desc]):
            res['result'] = False
            res['message'] = '你填写的数据不完整'

        # test_word = TestWord.objects.get(id=27)

        # 将数据保存到数据库中
        case_inse = CaseRegister()
        case_inse.function = function
        case_inse.dri = dri
        case_inse.desc = desc
        case_inse.save()
        res['result'] = True

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
