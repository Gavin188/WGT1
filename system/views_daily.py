import json

import pandas as pd
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from system.mixin import LoginRequiredMixin
from system.models import EngineerRank, VersionView, DutyView


class ExcelUpload(LoginRequiredMixin, View):
    '''测试说明书 视图'''

    def get(self, request):
        context = {

        }
        return render(request, 'system/ExcelUpload.html', context)

    def post(self, request):
        res = dict(result=False)
        f1 = request.FILES.get('f1')
        f2 = request.FILES.get('f2')
        f3 = request.FILES.get('f3')
        print(f1)
        print(f2)
        print(f3)
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
                df.drop(columns=['No.'])
                print('df', df)
                if list(df.columns) == ['No.', 'Name', 'Count']:
                    EngineerRank.objects.all().delete()
                    for i in range(len(df)):
                        # 写入数据库
                        rank = EngineerRank()
                        rank.name = df.loc[i, 'Name']
                        rank.count = df.loc[i, 'Count']
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
            print(res)
            return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
        # print(res)
        # return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
