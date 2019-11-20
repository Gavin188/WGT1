import datetime
import json

import pandas as pd
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from overtime.time_transformation import time_tran
from system.mixin import LoginRequiredMixin
from system.models import EngineerRank, VersionView, DutyView, UserProfile


class ExcelUpload(LoginRequiredMixin, View):
    '''测试说明书 视图'''

    def get(self, request):
        # context = {
        #
        # }
        return render(request, 'system/ExcelUpload.html')

    def post(self, request):
        res = dict(result=False)
        f1 = request.FILES.get('f1')
        f2 = request.FILES.get('f2')
        f3 = request.FILES.get('f3')
        # 上传Excel 文件
        if f1:
            if f1.name.endswith('.xlsx') or f1.name.endswith('.xls'):
                df = pd.read_excel(f1)
                df.fillna('', inplace=True)
                if list(df.columns) == ['日期', '版本', '平台']:
                    VersionView.objects.all().delete()
                    for i in range(len(df)):
                        # 写入数据库
                        version = VersionView()
                        version.date = df.loc[i, '日期']
                        version.version = df.loc[i, '版本']
                        version.platform = df.loc[i, '平台']
                        version.save()
                        res['msg'] = '上传成功！'
                        res['result'] = True

                else:
                    res['msg'] = "版本概览格式有誤"
                    res['result'] = False
                    return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
            else:
                res['msg'] = "请上传有效的文件"
                res['result'] = False
                return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
        if f2:
            if f2.name.endswith('.xlsx') or f2.name.endswith('.xls'):
                df = pd.read_excel(f2)
                df.fillna('', inplace=True)
                if list(df.columns) == ['日期', '名字']:
                    DutyView.objects.all().delete()
                    for i in range(len(df)):
                        # 写入数据库
                        duty = DutyView()
                        duty.weekend = df.loc[i, '日期']
                        duty.name = df.loc[i, '名字']
                        duty.date = datetime.date.today().strftime('%Y-%m-%d')
                        duty.save()
                        res['msg'] = '上传成功！'
                        res['result'] = True

                else:
                    res['msg'] = "值日概览格式有誤"
                    res['result'] = False
                    return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
            else:
                res['msg'] = "请上传有效的文件"
                res['result'] = False
                return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
        if f3:
            if f3.name.endswith('.xlsx') or f3.name.endswith('.xls'):
                df = pd.read_excel(f3)
                df.fillna('', inplace=True)
                # df.drop(columns=['No.'])
                if list(df.columns) == ['Originator', 'Count']:
                    # EngineerRank.objects.all().delete()
                    for i in range(len(df)):
                        # 写入数据库
                        name = list(UserProfile.objects.filter(radar=df.loc[i, 'Originator']))
                        rank = EngineerRank()
                        if name:
                            rank.name = df.loc[i, 'Originator']
                            rank.count = df.loc[i, 'Count']
                            rank.date = datetime.date.today().strftime('%Y-%m-%d')
                            rank.save()
                        res['msg'] = '上传成功！'
                        res['result'] = True

                else:
                    res['msg'] = "工程师排名格式有誤"
                    res['result'] = False
                    return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
            else:
                res['msg'] = "请上传有效的文件"
                res['result'] = False
                return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
        if res['result']:
            return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class HistoryManView(LoginRequiredMixin, View):
    '''显示 工程师 历史记录'''

    def get(self, request):
        today = datetime.date.today()  # - relativedelta(months=-1)
        next_date = today.strftime('%Y')
        next_moth = today.strftime('%m')
        context = {
            'next_date': next_date,
            'next_moth': next_moth,
        }
        return render(request, 'system/historyManager.html', context)

    def post(self, request):
        filters = {}

        res = {"success": "",
               "totalRows": "",
               "curPage": 1,
               "data": " "}
        # 获取 后台 查找 u用户
        person = request.POST.get('person')
        if request.POST.get('person'):
            filters['name__contains'] = person
        fields = ['id', 'name', 'count', 'date']
        # 获取查找的时间
        date = request.POST.get('date')
        moth = request.POST.get('moth')
        next_today = date + '-' + moth + '-01'
        month = time_tran(next_today)[0:7]
        #  查询出 未签核 和 已签核 加班时间
        filters['date__startswith'] = month
        datas = list(
            EngineerRank.objects.filter(**filters).values(*fields))

        #  先查询出 加班的所有用户 放入 arr_per
        data_list = []

        arr_per = []
        # 解析数据，将数据按照时间的字段
        for i in datas:
            if i['name'] not in arr_per:
                arr_per.append(i['name'])
        for per in arr_per:
            data_dict = {}
            count = 0
            for i in datas:
                if i['name'] == per:
                    data_dict['name'] = i['name']
                    data_dict['username'] = list(UserProfile.objects.filter(radar=i['name']).values('name'))[0][
                        'name']
                    data_dict[i['date'][8:10]] = i['count']
                    count = count + int(i['count'])
                    data_dict['Count'] = count
            data_list.append(data_dict)

        res["totalRows"] = len(datas)
        pageIndex = request.POST.get('curPage')
        pageSize = request.POST.get('pageSize')
        pageInator = Paginator(data_list, pageSize)
        contacts = pageInator.page(pageIndex)
        data_list = []  # 最终返回的结果集合
        for contact in contacts:
            data_list.append(contact)

        res["data"] = data_list

        res["curPage"] = pageIndex

        res['success'] = True
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class ExcelDeleteUpload(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        today = datetime.date.today().strftime('%Y-%m-%d')
        data = EngineerRank.objects.filter(date=today)
        if len(data) == 0:
            res['message'] = '今日的文件还没有上传！'
        else:
            data.delete()
            res['result'] = True

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
