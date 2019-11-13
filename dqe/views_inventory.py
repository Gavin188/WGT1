import json
from datetime import datetime
from itertools import chain

import pandas as pd
import requests
from django.core import serializers
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic.base import View

from dqe.get_mode import dynamicUpdateObjFields
from dqe.models import Project, Stage, OperateCacheTable, IpadDetails, ApplyListDetail, ApplyList
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu


# 庫存界面
# @method_decorator(login_required, name='dispatch') #测试3
class InventoryView(LoginRequiredMixin, View):  # class InventoryView(LoginRequiredMixin, View):

    # 测试2：使用装饰类实现，只有登陆用户才可以实现
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(InventoryView, self).dispatch(*args, **kwargs)
    # @method_decorator(login_required) 测试4

    def get(self, request):

        res = dict(data=IpadDetails.objects.all())
        # 專案
        projects = Project.objects.all()
        res['projects'] = projects

        # 階段
        stages = Stage.objects.all()

        res['stages'] = stages

        # 部門
        structures = Structure.objects.all()
        res['structures'] = structures

        # # 產品類型
        # prodtypes = ProductType.objects.all()
        # res['prodtypes'] = prodtypes

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)

        return render(request, 'dqe/Inventory/Inventory_List.html', res)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    def post(self, request):
        msg = ''  # 错误信息
        error_unit = []  # 错误项
        correct_unit = []  # 上传成功项
        repeat_unit = []  # 重複項
        '''
        >>> a = [[1, 2], [3, 4], [5, 6]]
        >>> list(itertools.chain.from_iterable(a))
        [1, 2, 3, 4, 5, 6]
        
        '''
        sn = list(chain.from_iterable(list(IpadDetails.objects.all().values_list("sn"))))  # 所有SN
        # print('2323', sn)
        if request.FILES.get("file"):
            file = request.FILES["file"]  # 获取上传的表格
            print('++', file)
            print('++', request.FILES)

            if file.name.endswith(".xlsx") or file.name.endswith(".xls"):  # 判断上传文件是否为表格
                df = pd.read_excel(file)

                # df.drop(0, axis=0, inplace=True)
                # 只要 有空 就将此行或者此列数据删除
                # df.dropna(inplace=True, how="any", axis=0)
                # df.dropna(inplace=True, how="any", axis=1)

                # 将空的数据替换
                df.fillna('', inplace=True, axis=0)
                df.fillna('', inplace=True, axis=1)

                df.drop('No', axis=1, inplace=True)
                # data = ['Platform', 'HW Build', 'WGT No.', 'Serial No.', 'Model', 'Status Detail', 'Fused',
                #         'Config', 'Display(TOPM)', 'NAND', 'In Date']
                # # units_status date_out recuser
                # df = df[data]

                for i in range(len(df)):
                    # 判斷表格中是否有重複信息
                    if str(df.loc[i, 'Serial No.'].replace(' ', '')) not in sn:
                        msg = "上傳成功"
                        correct_unit.append(df.loc[i].tolist())  # 成功上传的项
                        # data = ['Platform', 'HW Build', 'WGT No.', 'Serial No.', 'Model', 'Units Status', 'Status Detail', 'Fused',
                        #                     'Config','Display(TOPM)','NAND','In Date']
                        #             # units_status date_out recuser
                        ipaddetails = IpadDetails()
                        ipaddetails.platform = df.loc[i, 'Platform']
                        ipaddetails.hw_build = df.loc[i, 'HW Build']
                        ipaddetails.wgt_no = df.loc[i, 'WGT No.'].replace(' ', '')
                        ipaddetails.sn = str(df.loc[i, 'Serial No.'])

                        ipaddetails.model = df.loc[i, 'Model']
                        ipaddetails.status_detail = df.loc[i, 'Status Detail']
                        ipaddetails.fused = df.loc[i, 'Fused']
                        ipaddetails.config = df.loc[i, 'Config'].replace(' ', '')
                        ipaddetails.display = df.loc[i, 'Display(TOPM)'].replace(' ', '')
                        ipaddetails.nand = df.loc[i, 'NAND']
                        ipaddetails.date_in = df.loc[i, 'In Date']
                        ipaddetails.units_status = 1
                        ipaddetails.recuser = request.user.name  # 入库者

                        ipaddetails.hw_build_detail = df.loc[i, 'HW Build(Detail)']
                        ipaddetails.front_color = df.loc[i, 'Front Color']
                        ipaddetails.rear_color = df.loc[i, 'Rear Color']
                        ipaddetails.soc = df.loc[i, 'SOC']
                        ipaddetails.housing = df.loc[i, 'Housing']
                        ipaddetails.tm_grading = df.loc[i, 'TM Grading']
                        ipaddetails.grape = df.loc[i, 'Grape']
                        ipaddetails.nand_type = df.loc[i, 'NAND Type']
                        ipaddetails.die_name = df.loc[i, 'Die Name']
                        ipaddetails.battery_detail = df.loc[i, 'Battery Detail']
                        ipaddetails.battery_confirm = df.loc[i, 'Battery Confirm']
                        ipaddetails.mesa_flex = df.loc[i, 'Mesa Flex']
                        ipaddetails.wifi_vender = df.loc[i, 'WiFi Vender']
                        ipaddetails.WF1 = df.loc[i, 'WF1']
                        ipaddetails.wf2 = df.loc[i, 'WF2']
                        ipaddetails.wf3 = df.loc[i, 'WF3']
                        ipaddetails.wf5 = df.loc[i, 'WF5']
                        ipaddetails.wf5p = df.loc[i, 'WF5P']
                        ipaddetails.wf3_metrocirc = df.loc[i, 'WF3 Metrocirc']
                        ipaddetails.wf5_metrocirc = df.loc[i, 'WF5 Metrocirc']
                        ipaddetails.wf_sw_l = df.loc[i, 'WF_SW_L']
                        ipaddetails.wf_sw_r = df.loc[i, 'WF_SW_R']
                        ipaddetails.front_camera = df.loc[i, 'Front Camera']
                        ipaddetails.rear_camera = df.loc[i, 'Rear Camera']
                        ipaddetails.mikey_flex = df.loc[i, 'Mikey flex (Audio J Flex)']
                        ipaddetails.fh_spk = df.loc[i, 'FH L/R SPK']
                        ipaddetails.chin_spk = df.loc[i, 'Chin L/R SPK']
                        ipaddetails.spv_flex = df.loc[i, 'SPV Flex']
                        ipaddetails.microphone = df.loc[i, 'Microphone (Mic Flex)']
                        ipaddetails.microphone2 = df.loc[i, 'Microphone (Mic2 Flex)']
                        ipaddetails.c3_flex = df.loc[i, 'C3 Flex']
                        ipaddetails.c4_flex = df.loc[i, 'C4 Flex']
                        ipaddetails.mlb = df.loc[i, 'MLB']
                        ipaddetails.mlb_soc = df.loc[i, 'MLB Soc']
                        ipaddetails.pcb = df.loc[i, 'PCB']
                        ipaddetails.bash_flex = df.loc[i, 'Bash Flex']
                        ipaddetails.sim_flex = df.loc[i, 'SIM Flex']
                        ipaddetails.mimosa = df.loc[i, 'Mimosa']
                        ipaddetails.autobahn_flex = df.loc[i, 'Autobahn Flex']
                        ipaddetails.edp_flex = df.loc[i, 'EDP Flex']
                        ipaddetails.io_bonding = df.loc[i, 'IO Bonding']
                        ipaddetails.gyro_type = df.loc[i, 'Gyro Type']
                        ipaddetails.appleoscar = df.loc[i, 'AppleOscarAccelerometer(Accel)']
                        ipaddetails.dram = df.loc[i, 'DRAM']
                        ipaddetails.e75 = df.loc[i, 'E75 TriStar']
                        ipaddetails.full_lam = df.loc[i, 'Full Lam']
                        ipaddetails.unit_weight = df.loc[i, 'Unit Weight']
                        ipaddetails.ecid = df.loc[i, '16进制 ECID']
                        ipaddetails.apecid = df.loc[i, '10进制 APECID']
                        ipaddetails.snum = df.loc[i, 'SNUM']
                        ipaddetails.euicccsn = df.loc[i, 'EUICCCSN']
                        ipaddetails.unit_no = df.loc[i, 'Unit No.']
                        ipaddetails.aapn = df.loc[i, 'AAPN']
                        ipaddetails.hhpn = df.loc[i, 'HHPN']
                        ipaddetails.wo = df.loc[i, 'WO']
                        ipaddetails.allocatedto_group = df.loc[i, 'Allocated To/Group'].replace(' ', '')
                        ipaddetails.apple_dri = df.loc[i, 'Apple DRI']
                        ipaddetails.pt_no = df.loc[i, 'PT No.']
                        ipaddetails.apple_po = df.loc[i, 'Apple PO']
                        ipaddetails.boxsn = df.loc[i, '倉碼']
                        ipaddetails.certification_period = df.loc[i, '認證期限']
                        ipaddetails.accessory = df.loc[i, 'Accessory']
                        ipaddetails.presence_laser = df.loc[i, '有無鐳射']
                        ipaddetails.card = df.loc[i, '是否带卡']
                        ipaddetails.card_type = df.loc[i, '卡型号']
                        ipaddetails.detail_comment = df.loc[i, 'Detail Comment']

                        ipaddetails.save()
                        # else:
                        #     msg = "機台信息有誤"
                        #     error_unit.append(df.loc[i].tolist())  # 信息有误的项
                    else:
                        msg = "機台重复机台"
                        repeat_unit.append(df.loc[i].tolist())  # 重複機台

                ipad_data = list(IpadDetails.objects.filter().values('platform').distinct())
                da = [i['platform'] for i in ipad_data]
                project_data = list(Project.objects.filter().values('pname'))
                pro_da = [i['pname'] for i in project_data]

                for i in da:
                    if i not in pro_da:
                        project = Project()
                        project.pname = i
                        project.save()

                ipad_stage = list(IpadDetails.objects.filter().values('hw_build').distinct())
                da = [i['hw_build'] for i in ipad_stage]
                stage_data = list(Stage.objects.filter().values('sname'))
                sta_da = [i['sname'] for i in stage_data]
                for i in da:
                    if i not in sta_da:
                        project = Stage()
                        project.sname = i
                        project.save()
            else:
                msg = "請上傳表格文件"
            return render(request, 'dqe/Inventory/Inventory_upload_info.html',
                          {"msg": msg, "error_unit": error_unit, "correct_unit": correct_unit,
                           "repeat_unit": repeat_unit})

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++==
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++==


# 庫存列表
# @cache_page(60 * 15)
class InventoryListView(LoginRequiredMixin, View):
    def get(self, request):
        res = {
            "code": 0,
            "msg": "",
            "count": "",
            "data": "",
        }
        try:
            filters = {}

            data = serializers.serialize("json", IpadDetails.objects.filter(*filters).all().order_by('-date_in', 'id'))
            data = json.loads(data)
            count = len(data)
            print(count)
            all_page = []
            for record in data:
                record['fields']['pk'] = record['pk']
                fields = record['fields']
                all_page.append(fields)
            '''显示 分页'''
            pageIndex = request.GET.get('pageIndex', 1)  # 获取当前页数
            pageSize = request.GET.get('pageSize', 20)  # 获取每页的个数
            pageInator = Paginator(all_page, pageSize)
            contacts = pageInator.page(pageIndex)
            list = []  # 最终返回的结果集合
            for contact in contacts:
                list.append(contact)
            res['data'] = list
            res['count'] = count
            res['msg'] = True
        except ConnectionResetError:
            print('Handle Exception')

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 庫存 新增 和 修改
# get方式是跳转链接，而post方式是submit
class InventoryUpdateView(LoginRequiredMixin, View):
    # 注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):
        res = dict()
        return render(request, 'dqe/Inventory/Inventory_List.html', res)

    def post(self, request):
        res = dict(result=False)
        # # 新增数据 或者 更新 数组
        if request.POST.get("ID"):
            id = request.POST.get("ID")
            # print('2222----', id)
            value = request.POST.get('value')
            field = request.POST.get('field')
            if id != '':
                obj = IpadDetails.objects.get(id=id)

                # print('2222', obj)

                data = dynamicUpdateObjFields(obj=obj, fieldName=field,
                                              fieldValue=value)

                # print('datatat', data)

                res['result'] = True
                # print('reseres', res)
            else:
                id_record = IpadDetails()
        return HttpResponse(json.dumps(res), content_type='application/json')


# 库存批量删除
class InventoryDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        print('res', request.POST['id'])

        if 'id' in request.POST and request.POST['id']:
            data = request.POST.get('id').split(',')
            del data[len(data) - 1]

            id_list = map(int, data)

            for id in id_list:
                print(id)
                all_aceess = IpadDetails.objects.filter(id=id)
                all_aceess.delete()

            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# ipad 单个删除
class InventoryoneDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]
        # print(request.POST)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            IpadDetails.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# # 庫存機台出庫操作
# class InventoryOutView(LoginRequiredMixin, View):
#     def post(self, request):
#         print("++++++++++++++++++++")
#         res = dict(result=False)
#         id = list(map(int, request.POST.get('id').split(',')))[0]
#
#         if 'id' in request.POST and request.POST['id']:
#             id_list = map(int, request.POST.get('id').split(','))
#             list_inventory = Inventory.objects.filter(id__in=id_list)
#             for i_list_inventory in list_inventory:
#                 i_list_inventory.state = '4'
#                 i_list_inventory.save()
#                 print("更改成功！！！")
#             res['result'] = True
#
#         return HttpResponse(json.dumps(res), content_type='application/json')


# 查找 sn
class InventoryselectByOrderIdView(LoginRequiredMixin, View):
    def get(self, request):
        res = {
            "code": 0,
            "msg": "",
            "count": "1",
            "data": "",
        }
        orderId = request.GET.get('orderId')

        if orderId:
            data = serializers.serialize("json", IpadDetails.objects.filter(sn__contains=orderId).all())
            # print('232', data)
            data = json.loads(data)
            # print('data------', data)
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
            # res['count'] = count
            res['data'] = list
            res['msg'] = True
        else:
            res['msg'] = False
        print('sn1--', res)

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# # @Gavin 历史详细 ---没用到
# class InventoryDetailView(LoginRequiredMixin, View):
#     def get(self, request):
#         temp_id = request.GET.get('inventoryId')
#
#         # res = dict(data=Inventory.objects.all())
#         res = dict(apply=IpadDetails.objects.get(id=int(temp_id)))  # 獲取倉庫的信息   apply應該是inventory
#
#         # 思路
#         # 1.原始数据 : 查找Apply 和 ApplyDetail 中 fk_Inventory_id == 传递过来的id, 根据机台申请前状态，查找出该机台的原始数据
#         # 2.当前数据 : 遍历Inventory即为当前数据
#         # 3.历史数据 : 查找出Apply 和 ApplyDetail中所有 fk_inventory_id == 传递过来id的就可以。 这里可以独立出一个函数InventoryDetailListView
#
#         fields = ['id', 'fk_inventory__fk_project__pname', 'fk_inventory__fk_stage__sname', 'fk_inventory__rel',
#                   'fk_inventory__sn', 'indate', 'recuser', 'state', 'fk_structure__name', 'remark', 'currRecUser',
#                   'currRecDate'
#                   ]
#         filters = {}
#         # res['oridata'] = list(ApplyDetail.objects.filter(**filters).values(*fields, 'operatecachetable__opeuser').order_by('-indate'))
#
#         # now_time = datetime.now()
#         # lt = now_time - datetime.strptime(res['apply'].currRecDate, '%Y-%m-%d %H:%M:%S.%f')
#         # res['apply'].stayTime = str(lt.days) + "D" + " " + str(floor(lt.seconds / 60 / 60)) + "H"
#         # res['apply'].currRecDate = datetime.strptime(res['apply'].currRecDate, '%Y-%m-%d %H:%M:%S.%f')
#
#         menu = Menu.get_menu_by_request_url(url=self.request.path_info)
#         if menu is not None:
#             res.update(menu)
#
#         return render(request, 'dqe/Inventory/Inventory_Detail.html', res)


# @Gavin  新增机台
class InventoryInsertView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dqe/Inventory/Inventory_Update.html', None)

    def post(self, request):
        print(request.POST.get('units_status'))
        res = dict(result=False)
        ipaddetails = IpadDetails()
        ipaddetails.platform = request.POST.get('platform')
        ipaddetails.hw_build = request.POST.get('hw_build')
        ipaddetails.wgt_no = request.POST.get('wgt_no')
        ipaddetails.sn = request.POST.get('sn')
        ipaddetails.model = request.POST.get('model')
        ipaddetails.status_detail = request.POST.get('status_detail')
        ipaddetails.fused = request.POST.get('fused')
        ipaddetails.config = request.POST.get('config')
        ipaddetails.display = request.POST.get('display')
        ipaddetails.nand = request.POST.get('nand')
        ipaddetails.date_in = request.POST.get('date_in')
        ipaddetails.date_out = request.POST.get('date_out')
        ipaddetails.units_status = request.POST.get('units_status')
        ipaddetails.recuser = request.POST.get('recuser')

        ipaddetails.hw_build_detail = request.POST.get('hw_build_detail')
        ipaddetails.front_color = request.POST.get('front_color')
        ipaddetails.rear_color = request.POST.get('rear_color')
        ipaddetails.soc = request.POST.get('soc')
        ipaddetails.housing = request.POST.get('housing')
        ipaddetails.tm_grading = request.POST.get('tm_grading')
        ipaddetails.grape = request.POST.get('grape')
        ipaddetails.nand_type = request.POST.get('nand_type')
        ipaddetails.die_name = request.POST.get('die_name')
        ipaddetails.battery_detail = request.POST.get('battery_detail')
        ipaddetails.battery_confirm = request.POST.get('battery_confirm')
        ipaddetails.mesa_flex = request.POST.get('mesa_flex')
        ipaddetails.wifi_vender = request.POST.get('wifi_vender')
        ipaddetails.WF1 = request.POST.get('wf1')
        ipaddetails.wf2 = request.POST.get('wf2')
        ipaddetails.wf3 = request.POST.get('wf3')
        ipaddetails.wf5 = request.POST.get('wf5')
        ipaddetails.wf5p = request.POST.get('wf5p')
        ipaddetails.wf3_metrocirc = request.POST.get('wf3_metrocirc')
        ipaddetails.wf5_metrocirc = request.POST.get('wf5_metrocirc')
        ipaddetails.wf_sw_l = request.POST.get('wf_sw_l')
        ipaddetails.wf_sw_r = request.POST.get('wf_sw_r')
        ipaddetails.front_camera = request.POST.get('front_camera')
        ipaddetails.rear_camera = request.POST.get('rear_camera')
        ipaddetails.mikey_flex = request.POST.get('mikey_flex')
        ipaddetails.fh_spk = request.POST.get('fh_spk')
        ipaddetails.chin_spk = request.POST.get('chin_spk')
        ipaddetails.spv_flex = request.POST.get('spv_flex')
        ipaddetails.microphone = request.POST.get('microphone')
        ipaddetails.microphone2 = request.POST.get('microphone2')
        ipaddetails.c3_flex = request.POST.get('c3_flex')
        ipaddetails.c4_flex = request.POST.get('c4_flex')
        ipaddetails.mlb = request.POST.get('mlb')
        ipaddetails.mlb_soc = request.POST.get('mlb_soc')
        ipaddetails.pcb = request.POST.get('pcb')
        ipaddetails.bash_flex = request.POST.get('bash_flex')
        ipaddetails.sim_flex = request.POST.get('sim_flex')
        ipaddetails.mimosa = request.POST.get('mimosa')
        ipaddetails.autobahn_flex = request.POST.get('autobahn_flex')
        ipaddetails.edp_flex = request.POST.get('edp_flex')
        ipaddetails.io_bonding = request.POST.get('io_bonding')
        ipaddetails.gyro_type = request.POST.get('gyro_type')
        ipaddetails.appleoscar = request.POST.get('appleoscar')
        ipaddetails.dram = request.POST.get('dram')
        ipaddetails.e75 = request.POST.get('e75')
        ipaddetails.full_lam = request.POST.get('full_lam')
        ipaddetails.unit_weight = request.POST.get('unit_weight')
        ipaddetails.ecid = request.POST.get('ecid')
        ipaddetails.apecid = request.POST.get('apecid')
        ipaddetails.snum = request.POST.get('snum')
        ipaddetails.euicccsn = request.POST.get('euicccsn')
        ipaddetails.unit_no = request.POST.get('unit_no')
        ipaddetails.aapn = request.POST.get('aapn')
        ipaddetails.hhpn = request.POST.get('hhpn')
        ipaddetails.wo = request.POST.get('wo')
        ipaddetails.allocatedto_group = request.POST.get('allocatedto_group')
        ipaddetails.apple_dri = request.POST.get('apple_dri')
        ipaddetails.pt_no = request.POST.get('pt_no')
        ipaddetails.apple_po = request.POST.get('apple_po')
        ipaddetails.boxsn = request.POST.get('boxsn')
        ipaddetails.certification_period = request.POST.get('certification')
        ipaddetails.accessory = request.POST.get('accessory')
        ipaddetails.presence_laser = request.POST.get('presence_laser')
        ipaddetails.card = request.POST.get('card')
        ipaddetails.card_type = request.POST.get('card_type')
        ipaddetails.detail_comment = request.POST.get('detail_comment')
        ipaddetails.save()

        res['result'] = True

        # return render(request, 'dqe/Inventory/Inventory_List.html', res)
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# # 庫存機台入库操作
# class InventoryInView(LoginRequiredMixin, View):
#     def post(self, request):
#         # fk_structure__name
#         res = dict(result=False)
#         if 'id' in request.POST and request.POST['id']:
#             id_list = map(int, request.POST.get('id').split(','))
#             list_inventory = Inventory.objects.filter(id__in=id_list)
#             for i_list_inventory in list_inventory:
#                 i_list_inventory.state = '1'
#                 i_list_inventory.currRecUser = request.user.name
#                 i_list_inventory.fk_structure_id = request.user.department.id
#                 i_list_inventory.save()
#                 print("更改成功！！！")
#             res['result'] = True
#
#         return HttpResponse(json.dumps(res), content_type='application/json')


# 扫码 申请
'''
先扫码 获取 机台的SN
将获取的SN 如果在库存中 则 保存
如果不在库存中 ，则 将没有找到的SN 提交给仓管

'''


class InventoryScanApplyView(LoginRequiredMixin, View):
    # 注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):

        applyDetailId = request.GET.get('applyListDetailId')
        app_list = ApplyListDetail.objects.get(id=request.GET.get('applyListDetailId'))

        qty = app_list.qty

        return render(request, 'dqe/Inventory/ScanApply.html', {'applyDetailId': applyDetailId, 'qty': qty})

    def post(self, request):

        res = dict(result=False)

        sns = request.POST.get('sns').split('\r\n')
        app_list = ApplyListDetail.objects.get(id=request.GET.get('applydetailid'))
        apply_id = app_list.fk_apply_id

        # 思路：分两步 a.如果该sn存在库存中，那么将相应的Inventory_ID放入 OperateCacheTable 表中
        #          b.如果sn未在库存中找到，那么就将未找到的sn回应给客户

        #  STATE_TYPE = (("1", "入庫"), ("2", "已借出"), ("3", "出库"), ("4", "损坏"), ("5", "被外借"))
        invState2SN = []  # 将已经借出的 机台SN
        invState3SN = []  # 库存状态为已出库的SN
        invState4SN = []  # 损坏的sn
        invState1SN = []  # 已经保存到临时表中了
        invNotSN = []  # 将扫码没有的机台存放

        invState5SN = []  # 已经存在 临时表的 sn
        data = list(
            OperateCacheTable.objects.filter(fk_applylistdetail__fk_apply__id=apply_id).values('fk_inventory__sn'))
        for i in data:
            invState5SN.append(i['fk_inventory__sn'])
        print('data --- ', invState5SN)

        try:
            if request.user.department:  # 可能没登录，就获取不到

                for sn in sns:
                    if sn not in invState5SN:
                        invObj = IpadDetails.objects.filter(sn=sn)

                        # 判断对象是否存在，不存在表示该sn库存中没有
                        if invObj:
                            # 如果有对象 , 已经借出的、被申请、出库的不能进入缓存中，并提示相应信息
                            if invObj[0].units_status == '1':
                                OperateCacheTable.objects.get_or_create(
                                    fk_inventory=invObj[0],
                                    fk_applylistdetail=ApplyListDetail.objects.get(
                                        id=request.GET.get('applydetailid')),
                                    opeuser=request.user.name
                                )
                            else:
                                if invObj[0].units_status == '3':
                                    invState3SN.append(sn)  # 将被出库的sn归纳出来
                                elif invObj[0].units_status == '4':
                                    invState4SN.append(sn)  # 将损坏的sn归纳出来
                                elif invObj[0].units_status == '2':
                                    invState2SN.append(sn)  # 将损坏的sn归纳出来
                        else:
                            invNotSN.append(sn)
                    else:
                        invState1SN.append(sn)
            print(invState1SN)
            # 如果没有出现以下3种情况 則為1   # 1 表成功  2 表部分成功  3异常
            if invState3SN or invState4SN or invNotSN or invState2SN or invState1SN:
                if invState1SN:
                    res['invState1SN'] = invState1SN
                else:
                    res['invState1SN'] = '無'
                if invState3SN:
                    res['invState3SN'] = invState3SN
                else:
                    res['invState3SN'] = '無'
                if invState2SN:
                    res['invState2SN'] = invState2SN
                else:
                    res['invState2SN'] = '無'
                if invState4SN:
                    res['invState4SN'] = invState4SN
                else:
                    res['invState4SN'] = '無'

                if invNotSN:
                    res['invNotSN'] = invNotSN
                else:
                    res['invNotSN'] = '無'
                res['result'] = 2
            else:
                res['result'] = 1
        except Exception as e:

            res['result'] = 3

        return HttpResponse(json.dumps(res), content_type='application/json')


# 手动输入 wgt_no 将对应的sn 保存到申请机台表
class InventoryHandApplyView(LoginRequiredMixin, View):
    def get(self, request):
        applyDetailId = request.GET.get('applyListDetailId')
        app_list = ApplyListDetail.objects.get(id=request.GET.get('applyListDetailId'))

        qty = app_list.qty

        return render(request, 'dqe/Inventory/HandApply.html', {'applyDetailId': applyDetailId, 'qty': qty})

    def post(self, request):
        res = dict(result=False)
        sns = request.POST.get('sns').split('\r\n')

        app_list = ApplyListDetail.objects.get(id=request.GET.get('applydetailid'))
        apply_id = app_list.fk_apply_id

        invState5SN = []  # 已经存在 临时表的 sn
        data = list(
            OperateCacheTable.objects.filter(fk_applylistdetail__fk_apply__id=apply_id).values('fk_inventory__wgt_no'))
        for i in data:
            invState5SN.append(i['fk_inventory__wgt_no'])
        print('data --- ', invState5SN)

        #  STATE_TYPE = (("1", "入庫"), ("2", "已借出"), ("3", "出库"), ("4", "损坏"), ("5", "被外借"))
        invState1SN = []  # 将已经存在临时表的 机台SN
        invState2SN = []  # 将已经借出的 机台SN
        invState3SN = []  # 库存状态为已出库的SN
        invState4SN = []  # 库存状态为已损坏的SN
        invNotSN = []  # 将扫码没有的机台存放

        try:
            if request.user.department:  # 可能没登录，就获取不到

                for wgt in sns:
                    if wgt not in invState5SN:
                        invObj = IpadDetails.objects.filter(wgt_no=wgt)

                        # 判断对象是否存在，不存在表示该sn库存中没有
                        if invObj:
                            # 如果有对象 , 已经借出的、被申请、出库的不能进入缓存中，并提示相应信息
                            if invObj[0].units_status == '1':
                                OperateCacheTable.objects.get_or_create(
                                    fk_inventory=invObj[0],
                                    fk_applylistdetail=ApplyListDetail.objects.get(
                                        id=request.GET.get('applydetailid')),
                                    opeuser=request.user.name
                                )
                            else:
                                if invObj[0].units_status == '3':
                                    invState3SN.append(wgt)  # 将被出库的sn归纳出来
                                elif invObj[0].units_status == '4':
                                    invState4SN.append(wgt)  # 将损坏的sn归纳出来
                                elif invObj[0].units_status == '2':
                                    invState2SN.append(wgt)  # 将已经借出的sn归纳出来
                        else:
                            invNotSN.append(wgt)
                    else:
                        invState1SN.append(wgt)
            # 如果没有出现以下3种情况 則為1   # 1 表成功  2 表部分成功  3异常
            if invState3SN or invState4SN or invNotSN or invState2SN or invState1SN:
                if invState1SN:
                    res['invState1SN'] = invState1SN
                else:
                    res['invState1SN'] = '無'
                if invState3SN:
                    res['invState3SN'] = invState3SN
                else:
                    res['invState3SN'] = '無'
                if invState2SN:
                    res['invState2SN'] = invState2SN
                else:
                    res['invState2SN'] = '無'
                if invState4SN:
                    res['invState4SN'] = invState4SN
                else:
                    res['invState4SN'] = '無'

                if invNotSN:
                    res['invNotSN'] = invNotSN
                else:
                    res['invNotSN'] = '無'
                res['result'] = 2
            else:
                res['result'] = 1
        except Exception as e:

            res['result'] = 3

        return HttpResponse(json.dumps(res), content_type='application/json')


# @Gavin  扫码还机台
class InventoryScanReturnView(LoginRequiredMixin, View):
    def get(self, request):
        applyDetailId = request.GET.get('applyListDetailId')
        print('--id', applyDetailId)
        # app_list = ApplyListDetail.objects.get(id=applyDetailId)
        # print('++++', app_list)
        # qty = app_list.qty

        return render(request, 'dqe/Inventory/ScanReturn.html', {'applyDetailId': applyDetailId})

    def post(self, request):
        res = dict(result=False)
        sns = request.POST.get('sns').split('\r\n')
        apply_id = request.GET.get('id')
        print('--==--', apply_id)
        data = list(OperateCacheTable.objects.filter(fk_applylistdetail__fk_apply_id=apply_id).values_list(
            'fk_inventory__sn'))
        all_sns = []
        for i in range(len(data)):
            all_sns.append(data[i][0])

        # print('all--', all_sns)
        invalidSn = []  # 无效的sn
        if request.user.department:

            for sn in sns:
                if sn in all_sns:
                    data = OperateCacheTable.objects.filter(fk_inventory__sn=sn)
                    for da in data:
                        da.fk_inventory.units_status = 1
                        da.returnDate = datetime.now()
                        da.fk_inventory.save()
                        da.save()
                else:
                    invalidSn.append(sn)

            # arr = [i for i in all_sns for j in sns if i == j]
            # # print(arr)
            # if arr:
            #     for sn in arr:
            #         data = OperateCacheTable.objects.get(fk_inventory__sn=sn)
            #         # print('data--', data)
            #         data.fk_inventory.units_status = 1
            #         data.returnDate = datetime.now()
            #         data.fk_inventory.save()
            #         data.save()
            #     res['result'] = True
            # else:
            #     invalidSn.append(arr)

        # 如果没有出现以下3种情况 則為1   # 1 表成功  2 表部分成功

        if invalidSn:
            res['invalidSn'] = invalidSn
            res['result'] = 2
        else:
            res['invStateSN'] = '無'
            res['result'] = 1

        status = OperateCacheTable.objects.filter(fk_applylistdetail__fk_apply_id=apply_id).values(
            'fk_inventory__units_status').distinct()
        flag = True

        for i in status:
            if int(i['fk_inventory__units_status']) == 2:
                flag = False
                break
        if flag:
            da = ApplyList.objects.get(id=apply_id)
            da.applyState = 3
            da.save()

        return HttpResponse(json.dumps(res), content_type='application/json')
