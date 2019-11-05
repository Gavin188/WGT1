# Create your views here.
import json

import pandas as pd
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from system.mixin import LoginRequiredMixin

#  案例管理
from system.models import TestWord
from testManage.models import CaseRegister, TestFun


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

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class CaseFunFindView(LoginRequiredMixin, View):
    '''案例管理 - 显示测试项的具体测试功能'''

    def get(self, request):
        id = request.GET.get('id')
        # 将测试项传入后台
        case = list(CaseRegister.objects.filter(id=id).values())[0]
        context = {
            'case': case
        }
        return render(request, 'testManage/Case_fun.html', context)

    def post(self, request):
        res = dict(result=False)
        file = request.FILES.get("file")
        case_id = request.POST.get('case_id')
        if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
            df = pd.read_excel(file)
            df.fillna('', inplace=True)
            if list(df.columns) == ['用例编号', '功能', '操作步骤', '预期结果']:
                try:
                    case = CaseRegister.objects.get(id=case_id)
                    for i in range(len(df)):
                        test_fun = TestFun()
                        test_fun.fk_case = case
                        test_fun.case_id = df.loc[i, '用例编号']
                        test_fun.function = df.loc[i, '功能']
                        test_fun.oper_step = df.loc[i, '操作步骤']
                        test_fun.expect = df.loc[i, '预期结果']
                        test_fun.upload_user = request.user
                        test_fun.save()
                        res['msg'] = '上传成功！'
                        res['result'] = True
                except Exception:
                    res['msg'] = "不存在测试项"
                    res['result'] = False
            else:
                res['msg'] = "表格格式有誤"
                res['result'] = False
        else:
            res['errmsg'] = '请上传有效的文件'
            res['result'] = False
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class CaseDescIroView(LoginRequiredMixin, View):
    '''案例管理 - 显示测试说明的测试文档'''

    def get(self, request):
        print(request.GET)
        # 测试说明的文档字段
        fields = ['id', 'title', 'publisher', 'desc_pack']
        errmsg = ''
        flag = ''
        result = ''
        # # todo: 案例管理： 获取相对应的测试项测试说明，名称
        if 'id' in request.GET and request.GET['id']:
            id = request.GET.get('id')
            # 获取测试项的名称
            try:
                title = list(CaseRegister.objects.filter(id=id).values('desc'))[0]['desc']
            except Exception:
                errmsg = '用例编号不存在'
                result = True
            # 判断 测试说明文档中是否存在 相应的文档
            all_obj = list(TestWord.objects.filter(title=title).values(*fields))
            # 如果没有存在则提示
            if len(all_obj) == 0:
                errmsg = '还没有添加测试说明'
                flag = True
                result = True
        # todo: 今日测试 - 获取测试项
        if 'comment' in request.GET and request.GET['comment']:
            comment = request.GET.get('comment')
            print('comment --', comment)
            # 获取测试项的名称
            try:
                title = list(CaseRegister.objects.filter(function=comment).values('desc'))[0]['desc']
            except Exception:
                errmsg = '用例编号不存在'
                result = True
                title = ''
            # 判断 测试说明文档中是否存在 相应的文档
            # print('titie--', title)
            print(errmsg)
            print(result)
            if result:
                print(1111)
                all_obj = ''

            else:
                all_obj = list(TestWord.objects.filter(title=title).values(*fields))
            # 如果没有存在则提示
            if len(all_obj) == 0:
                errmsg = '还没有添加测试说明'
                flag = False
                result = True

        context = {
            'flag': flag,
            'title': title,
            'all': all_obj,
            'result': result,
            'errmsg': errmsg
        }

        return render(request, 'system/Test_Word/DetailWord.html', context)


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
            return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
        # 判断测试项是否重复。
        fun = CaseRegister.objects.filter(function=function)
        if fun:
            res['result'] = False
            res['message'] = '你填写的测试项已存在'
            return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')

        # 判断测试说明是否重复
        word = TestWord.objects.filter(title=desc)
        if word:
            res['result'] = False
            res['message'] = '你填写的测试说明已存在'
            return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')

        # 将数据保存到数据库中
        case_inse = CaseRegister()
        case_inse.function = function
        case_inse.dri = dri
        case_inse.desc = desc
        case_inse.save()
        res['result'] = True
        print(res)
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class CaseFunListView(LoginRequiredMixin, View):
    '''显示测试功能模块'''

    def post(self, request, case_id):
        res = {"success": "",
               "totalRows": "",
               "curPage": "",
               "data": " ", }
        data = list(TestFun.objects.filter(fk_case__id=case_id).values())
        count = len(data)
        # 进行分页
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
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class CaseFunDelView(LoginRequiredMixin, View):
    '''删除测试功能模块'''

    def post(self, request):
        res = dict(result=False)
        case_id = request.POST.get('case_id')
        try:
            TestFun.objects.filter(fk_case__id=case_id).delete()
            res['result'] = True
        except Exception:
            res['result'] = False
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
