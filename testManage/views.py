import datetime
import json

import pandas as pd
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views import View

from system.mixin import LoginRequiredMixin
from system.models import UserProfile
from testManage.models import TaskArrange, TimeArrange


class TaskArrangeView(LoginRequiredMixin, View):
    '''任务安排首页'''

    def get(self, request):
        res = dict()
        # 获取当前时间
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        res['data'] = today
        return render(request, 'testManage/TaskArrange.html', {'data': res})

    def post(self, request):
        res = dict(result=False)
        file = request.FILES.get("file")
        # 上传Excel 文件
        if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
            df = pd.read_excel(file)
            df.fillna('', inplace=True)
            if list(df.columns) == ['WGT No.', 'Serial No', 'Fused', 'NAND', 'Test Build', 'Tester', 'Comments']:
                # data_list = []
                # # 将数据中所有的人和测试项 提取出来，判断是否有重复的测试人
                # for i in range(len(df)):
                #     data1 = df.iloc[i, df.columns.get_indexer(['Tester', 'Comments'])]
                #     tester = data1['Tester']
                #     comments = data1['Comments']
                #     # 将测试项和测试人 保存成字典类型
                #     data_dict = dict(key=tester, value=comments)
                #     if data_dict not in data_list:
                #         data_list.append(data_dict)
                # # 判断是否存在 一人 -> 多个测试项
                # flag = True
                # tester_list = []
                # tester1_list = []
                # for i in data_list:
                #     tester = i['key']
                #     if tester in tester_list:
                #         flag = False
                #         tester1_list.append(tester)
                #     else:
                #         tester_list.append(tester)
                # if flag:
                time_arrange = TimeArrange()
                time_arrange.pub_date = datetime.date.today()
                time_arrange.save()
                for i in range(len(df)):
                    # 写入数据库
                    arrange = TaskArrange()
                    arrange.task_date = time_arrange
                    arrange.wgt_no = df.loc[i, 'WGT No.']
                    arrange.serial_no = df.loc[i, 'Serial No'].replace(' ', '')
                    arrange.fused = df.loc[i, 'Fused']
                    arrange.nand = df.loc[i, 'NAND'].replace(' ', '')
                    arrange.test_build = df.loc[i, 'Test Build']
                    arrange.tester = df.loc[i, 'Tester']
                    arrange.comments = df.loc[i, 'Comments']
                    arrange.upload_user = request.user
                    arrange.save()
                    res['msg'] = '上传成功！'
                    res['result'] = True
                # else:
            #     res['msg'] = str(tester1_list) + "测试员对应多个测试项，请检查"
            #     res['result'] = False
            else:
                res['msg'] = "表格格式有誤"
                res['result'] = False
        else:
            res['msg'] = "请上传有效的文件"
            res['result'] = False
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class TaskArrangeListView(LoginRequiredMixin, View):
    '''今日测试首页列表'''

    def post(self, request):
        res = {"success": "",
               "totalRows": "",
               "curPage": "",
               "data": " "}
        fields = ['id', 'wgt_no', 'serial_no', 'fused', 'nand', 'test_build', 'tester', 'comments', 'upload_user',
                  'task_date__pub_date']

        searchFields = ['tester', 'wgt_no', 'task_date__pub_date']  # 与数据库字段一致 'find_per', 'indate'
        filters = {i + '__icontains': request.POST.get(i, '') for i in searchFields if
                   i not in ['tester', 'wgt_no',
                             'task_date__pub_date', ]}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        # 通过id筛选数据，id必须是确定的，如果id不存在，那么不将该条件放入
        if request.POST.get('tester'):
            filters['tester'] = request.POST.get('tester')
        if request.POST.get('wgt_no'):
            filters['wgt_no'] = request.POST.get('wgt_no')

        if request.POST.get('pub_date'):
            filters['task_date__pub_date'] = request.POST.get('pub_date')
        else:
            filters['task_date__pub_date'] = datetime.date.today()

        data = list(TaskArrange.objects.filter(**filters).values(*fields))
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


class TaskArrangeDeleteView(LoginRequiredMixin, View):
    '''删除当天任务'''

    def post(self, request):
        res = dict(result=False)
        pub_data = request.POST.get('pub_data')
        if pub_data:
            TimeArrange.objects.filter(pub_date=pub_data).delete()
            res['result'] = True
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class TaskArrangeRearchView(LoginRequiredMixin, View):
    '''联想记忆法 - 姓名'''

    def post(self, request):
        res = dict(result=False)
        uname = request.POST.get('search')
        if uname:
            user = list(UserProfile.objects.filter(name__contains=uname).values('name').distinct())

            user_name = [i['name'] for i in user]

            res['username'] = user_name
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class TaskArrangeRearchWGTView(LoginRequiredMixin, View):
    '''联想记忆法 wgt_no'''

    def post(self, request):
        res = dict(result=False)
        wgt_no = request.POST.get('search')
        if wgt_no:
            wgt_nos = list(TaskArrange.objects.filter(wgt_no__icontains=wgt_no).values('wgt_no').distinct()[:33])

            wgt_nos = [i['wgt_no'] for i in wgt_nos]

            res['username'] = wgt_nos
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
