import json
from itertools import chain
import json
from itertools import chain

import pandas as pd
from django.core import serializers
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from dqe.models import OperateCacheTable, Project, Stage, AccessDetails
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu, Access


# @Gavin  配件信息表
class OperateCacheTableView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=OperateCacheTable.objects.all())

        # 專案
        projects = Project.objects.all()
        res['projects'] = projects

        # 階段
        stages = Stage.objects.all()
        res['stages'] = stages

        # 部門
        structures = Structure.objects.all()
        res['structures'] = structures

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)
        # print(res)
        return render(request, 'dqe/OperateCacheTable/OperateCacheTable_List.html', res)

    def post(self, request):
        msg = ""  # 错误信息
        error_unit = []  # SN 为空
        correct_unit = []  # 上传成功项
        repeat_unit = []  # 重複項
        '''
        >>> a = [[1, 2], [3, 4], [5, 6]]
        >>> list(itertools.chain.from_iterable(a))
        [1, 2, 3, 4, 5, 6]
        
        '''
        sn = list(chain.from_iterable(list(AccessDetails.objects.all().values_list("sn"))))  # 所有SN

        # 上传 文件  并且 解析excel
        # file = request.FILES["file"]  # 获取上传的表格
        if request.FILES.get("file"):
            file = request.FILES["file"]  # 获取上传的表格
            if file.name.endswith(".xlsx") or file.name.endswith(".xls"):  # 判断上传文件是否为表格

                df = pd.read_excel(file)
                df.fillna('', inplace=True)
                for i in range(len(df)):
                    if df.loc[i, "Date in"] == '':
                        df.loc[i, "Date in"] = '1900-01-01'
                    elif type(df.loc[i, "Date in"]) is not str:
                        df.loc[i, "Date in"] = df.loc[i, "Date in"].strftime("%Y-%m-%d")

                for i in range(len(df)):
                    if str(df.loc[i, 'SN']) != "":
                        if str(df.loc[i, 'SN']).replace(' ', '') not in sn:
                            msg = "上传成功"
                            correct_unit.append(df.loc[i].tolist())
                            # Accessory	Vender	HW Build	Config	Status	Qty.	盒子SN	SN
                            # Contact & Address	Date in	Date Out	Comment	仓码	储位	AAPN	HHPN	WO
                            accessDetails = AccessDetails()

                            # 將數據寫入數據庫
                            accessDetails.accessory = df.loc[i, 'Accessory'].replace(' ', '')
                            accessDetails.vender = df.loc[i, 'Vender'].replace(' ', '')
                            accessDetails.hw_build = df.loc[i, 'HW Build'].replace(' ', '')
                            accessDetails.config = str(df.loc[i, 'Config']).replace(' ', '')
                            # accessDetails.status = df.loc[i, 'Status'].replace(' ', '')
                            accessDetails.status = 2
                            accessDetails.recuser = request.user.name
                            accessDetails.qty = df.loc[i, 'Qty.']
                            accessDetails.box_sn = df.loc[i, '盒子SN'].replace(' ', '')
                            accessDetails.sn = str(df.loc[i, 'SN'])
                            accessDetails.contact_address = df.loc[i, ' Contact & Address']
                            accessDetails.date_in = str(df.loc[i, 'Date in'])
                            accessDetails.date_out = df.loc[i, 'Date Out']
                            accessDetails.comment = df.loc[i, 'Comment'].replace(' ', '')
                            accessDetails.ca_sn = df.loc[i, '仓码']
                            accessDetails.store = df.loc[i, '储位']
                            accessDetails.aapn = df.loc[i, 'AAPN']
                            accessDetails.hhpn = df.loc[i, 'HHPN']
                            accessDetails.wo = df.loc[i, 'WO']

                            accessDetails.save()

                        else:
                            msg = "重复机台"
                            repeat_unit.append(df.loc[i].tolist())
                    else:
                        msg = "SN 不能为空"
                        error_unit.append(df.loc[i].tolist())

                access_data = list(AccessDetails.objects.filter().values('accessory').distinct())
                da = [i['accessory'] for i in access_data]
                access_data = list(Access.objects.filter().values('access'))
                access_da = [i['access'] for i in access_data]
                for i in da:
                    if i not in access_da:
                        access = Access()
                        access.access = i
                        access.save()

            else:
                msg = "請上傳表格文件"

            return render(request, 'dqe/OperateCacheTable/Accessory_upload_info.html',
                          {"msg": msg, "correct_unit": correct_unit, "repeat_unit": repeat_unit})

        # # 新增数据 或者 更新 数组
        if request.POST.get("ID"):
            # print(request.POST.get("Status"))

            id = request.POST.get("ID")
            if id != '':
                id_record = AccessDetails.objects.get(id=id)
        else:
            id_record = AccessDetails()
        # print('--', request.POST.get("Status"))
        id_record.accessory = request.POST.get('Accessory')
        id_record.vender = request.POST.get("Vender")
        id_record.hw_build = request.POST.get("hw_build")
        id_record.config = request.POST.get("Config")
        id_record.status = request.POST.get("Status")

        id_record.qty = request.POST.get("QTY")
        id_record.box_sn = request.POST.get("box_sn")
        id_record.sn = request.POST.get("SN")
        id_record.contact_address = request.POST.get("Contact&Address")
        id_record.date_in = request.POST.get("Date In")
        # id_record.date_out = request.POST.get("date_out")
        id_record.comment = request.POST.get("comment")
        id_record.ca_sn = request.POST.get("cat_sn")
        id_record.store = request.POST.get("Store")
        id_record.aapn = request.POST.get("AAPN")
        id_record.hhpn = request.POST.get("HHPN")
        id_record.wo = request.POST.get("WO")
        id_record.save()

        return render(request, 'dqe/OperateCacheTable/OperateCacheTable_List.html', None)


# 操作緩存 列表
class OperateCacheTableListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'accessory', 'vender', 'hw_build', 'config',
                  'status', 'qty', 'box_sn', 'sn',
                  'contact_address', 'date_in', 'date_out', 'comment',
                  'ca_sn',
                  'store', 'aapn', 'hhpn', 'wo', 'recuser'
                  ]
        filters = {}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        res = {
            "code": 0,
            "msg": "",
            "count": "",
            "data": "",
        }

        # res = dict(data=list(AccessDetails.objects.filter(**filters).values(*fields)))

        data = serializers.serialize("json", AccessDetails.objects.all().order_by('-date_in', 'id'))
        count = AccessDetails.objects.all().count()
        data = json.loads(data)
        # print('data', data)
        all_page = []
        for record in data:
            record['fields']['pk'] = record['pk']
            fields = record['fields']
            all_page.append(fields)
        '''显示 分页'''
        # print('all_page', all_page)
        pageIndex = request.GET.get('pageIndex')  # pageIndex = request.POST.get('pageIndex')
        pageSize = request.GET.get('pageSize')  # pageSize = request.POST.get('pageSize')
        pageInator = Paginator(all_page, pageSize)

        contacts = pageInator.page(pageIndex)

        # print('1', pageIndex)
        # print('2', pageSize)
        # print('3', pageInator)
        # print('4', contacts)

        list = []  # 最终返回的结果集合
        for contact in contacts:
            # print(contact)
            list.append(contact)
        res['count'] = count
        res['data'] = list
        res['msg'] = True
        # print(res)

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class OperateCacheTableUpdateView(LoginRequiredMixin, View):
    # def get(self, request):
    #     res = dict()
    #
    #     if 'id' in request.GET and request.GET['id']:
    #         oct = get_object_or_404(OperateCacheTable, pk=request.GET.get('id'))
    #         res['oct'] = oct
    #     else:
    #         octs = OperateCacheTable.objects.all()
    #         res['octs'] = octs
    #
    #     return render(request, 'dqe/OperateCacheTable/OperateCacheTable_Update.html', res)

    # def post(self, request):
    #     res = dict(result=False)
    #     if 'id' in request.POST and request.POST['id']:  # id的存在，就是为了说明是新增数据还是编辑数据
    #         oct = get_object_or_404(OperateCacheTable, pk=request.POST.get('id'))
    #     else:
    #         oct = OperateCacheTable()
    #
    #     oct_create_form = OperateCacheTableCreateForm(request.POST, instance=oct)
    #
    #     if oct_create_form.is_valid():
    #         oct_create_form.save()
    #         res['result'] = True
    #
    #     return HttpResponse(json.dumps(res), content_type='application/json')

    def post(self, request):
        # 获取单条记录到表单
        # print(111144444)
        response = serializers.serialize("json", AccessDetails.objects.filter(id=request.POST.get('id')))
        response = json.loads(response)
        # print('response', response)
        return2ajax = {}
        return2ajax["record"] = response[0]["fields"]
        # print('return2ajax', return2ajax)

        return HttpResponse(json.dumps(return2ajax, cls=DjangoJSONEncoder), content_type='application/json')


# 删除配件库存  批量 删除操作
class OperateCacheTableDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        print('res', request.POST['id'])
        # data = request.POST.get('id').split(',')
        # del data[:0]
        print('11111', request.POST)

        if 'id' in request.POST and request.POST['id']:
            data = request.POST.get('id').split(',')
            del data[len(data) - 1]

            id_list = map(int, data)

            for id in id_list:
                print(id)
                all_aceess = AccessDetails.objects.filter(id=id)
                all_aceess.delete()

            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 单个删除
class AccessoryDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            AccessDetails.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 申请确认
# 思路：创建Apply>将ApplyDetail也创建出来>清空操作缓存>库存中的状态变为被申请状态
class AcceselectByOrderIdView(LoginRequiredMixin, View):
    def get(self, request):

        res = {
            "code": 0,
            "msg": "",
            "count": "1",
            "data": "",
        }
        orderId = request.GET.get('orderId')

        if orderId:
            data = serializers.serialize("json", AccessDetails.objects.filter(sn__contains=orderId).all())
            data = json.loads(data)
            all_page = []
            for record in data:
                record['fields']['pk'] = record['pk']
                fields = record['fields']
                all_page.append(fields)
            '''显示 分页'''
            pageIndex = request.GET.get('pageIndex')  # pageIndex = request.POST.get('pageIndex')
            pageSize = request.GET.get('pageSize')  # pageSize = request.POST.get('pageSize')
            pageInator = Paginator(all_page, pageSize)

            contacts = pageInator.page(pageIndex)

            list = []  # 最终返回的结果集合
            for contact in contacts:
                # print(contact)
                list.append(contact)
            # res['count'] = count
            res['data'] = list
            res['msg'] = True
        else:
            res['msg'] = False

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
