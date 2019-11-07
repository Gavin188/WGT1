# Create your views here.
import datetime
import json

import pandas as pd
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from system.mixin import LoginRequiredMixin
#  案例管理
from testManage.models import BugRegister
from testManage.tests import dynamicUpdateObjFields


class BugRegisterView(LoginRequiredMixin, View):
    def get(self, request):
        time = datetime.datetime.now().strftime("%Y-%m-%d")
        return render(request, 'testManage/BugRegister.html', {'time': time})

    def post(self, request):
        res = dict(result=False)
        file = request.FILES.get("file")
        print(file)

        if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
            df = pd.read_excel(file)
            df.fillna('', inplace=True)
            # 日期	组别	发现人	提报人	Radar ID	描述	备注
            if list(df.columns) == ['日期', '组别', '发现人', '提报人', 'Radar ID', '描述', '备注']:
                for i in range(len(df)):
                    # 写入数据库
                    bug = BugRegister()
                    bug.date = df.loc[i, '日期']
                    bug.group = df.loc[i, '组别'].replace(' ', '')
                    bug.find_per = df.loc[i, '发现人']
                    bug.sub_per = df.loc[i, '提报人'].replace(' ', '')
                    bug.radar_id = df.loc[i, 'Radar ID']
                    bug.desc = df.loc[i, '描述']
                    bug.comments = df.loc[i, '备注']
                    bug.save()
                    res['msg'] = '上传成功！'
                    res['result'] = True
            else:
                res['msg'] = "表格格式有誤"
                res['result'] = False
        else:
            res['msg'] = "请上传有效的文件"
            res['result'] = False

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


#  案例管理列表
class BugRegisterListView(LoginRequiredMixin, View):
    def post(self, request):
        res = {"success": "",
               "totalRows": "",
               "curPage": "",
               "data": " "}
        fields = ['id', 'date', 'group', 'find_per', 'sub_per', 'radar_id', 'desc', 'comments']
        data = list(BugRegister.objects.values(*fields).order_by('-date'))
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


#  新增bug数据
class BugRegisterSaveView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        data = dict(request.POST)
        print(data)
        if len(data['radar_id'][0]) != 0:
            bug_register = BugRegister()
            bug_register.date = data['date'][0]
            bug_register.group = data['group'][0]
            bug_register.find_per = data['find_per'][0]
            bug_register.sub_per = data['sub_per'][0]
            bug_register.radar_id = data['radar_id'][0]
            bug_register.desc = data['desc'][0]
            bug_register.comments = data['comments'][0]
            bug_register.save()
            res['result'] = True

        else:
            res['msg'] = '雷达不能为空'

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 更新bug 登记 数据
class BugRegisterUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        data222 = request.POST
        print('data2222', data222)
        data = dict(data222)
        obj = BugRegister.objects.get(id=int(data['id'][0]))
        radar_id = data['radar_id'][0]
        desc = data['desc'][0]
        comments = data['comments'][0]
        if radar_id != '[object Object]':
            radar_id = dynamicUpdateObjFields(obj=obj, fieldName='radar_id',
                                              fieldValue=str(radar_id))
            res['result'] = True
        if desc != '[object Object]':
            desc = dynamicUpdateObjFields(obj=obj, fieldName='desc',
                                          fieldValue=str(desc))
            res['result'] = True
        if comments != '[object Object]':
            comments = dynamicUpdateObjFields(obj=obj, fieldName='comments',
                                              fieldValue=str(comments))
            res['result'] = True
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 删除bug登记 数据
class BugRegisterDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        bug_id = request.POST.get('id')
        if bug_id:
            BugRegister.objects.filter(id=int(bug_id)).delete()
            res['result'] = True
        else:
            res['result'] = False
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# bug 记录
class BugRemarkView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'testManage/BugRemark.html', None)


# bug 记录详情
class BugRemarkListView(LoginRequiredMixin, View):
    def post(self, request):
        res = {"success": "",
               "totalRows": "",
               "curPage": "",
               "data": " "}
        fields = ['id', 'date', 'group', 'find_per', 'sub_per', 'radar_id', 'desc', 'comments']

        # date = request.POST.get('date')
        # sub_per = request.POST.get('sub_per')
        # find_per = request.POST.get('find_per')

        searchFields = ['date', 'sub_per', 'find_per']  # 与数据库字段一致 'find_per', 'indate'
        filters = {i + '__icontains': request.POST.get(i, '') for i in searchFields if
                   i not in ['date', 'sub_per',
                             'find_per', ]}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
        print(filters)

        # 通过id筛选数据，id必须是确定的，如果id不存在，那么不将该条件放入
        if request.POST.get('date'):
            filters['date'] = request.POST.get('date')
        if request.POST.get('sub_per'):
            filters['sub_per'] = request.POST.get('sub_per')
        if request.POST.get('find_per'):
            filters['find_per'] = request.POST.get('find_per')
        data = list(
            BugRegister.objects.filter(**filters).values(*fields).order_by('-date'))
        count = len(data)

        # data = list(BugRegister.objects.values(*fields).order_by('-date'))
        # count = len(data)
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
