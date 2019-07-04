import json
from datetime import datetime
from itertools import chain
from math import floor

import pandas as pd
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import View

from dqe.forms import InventoryCreateForm
from dqe.models import Inventory, Project, Stage, OperateCacheTable, ApplyDetail, ProductType
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

        res = dict(data=Inventory.objects.all())
        # 專案
        projects = Project.objects.all()
        res['projects'] = projects

        # 階段
        stages = Stage.objects.all()

        res['stages'] = stages

        # 部門
        structures = Structure.objects.all()
        res['structures'] = structures

        # 產品類型
        prodtypes = ProductType.objects.all()
        res['prodtypes'] = prodtypes

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
        sn = list(chain.from_iterable(list(Inventory.objects.all().values_list("sn"))))  # 所有SN

        file = request.FILES["file"]  # 获取上传的表格

        if file.name.endswith(".xlsx") or file.name.endswith(".xls"):  # 判断上传文件是否为表格
            df = pd.read_excel(file)

            df.dropna(inplace=True, how="any", axis=0)
            df.dropna(inplace=True, how="any", axis=1)

            for i in range(len(df)):
                if list(df.columns) == ['專案', '階段', '編號', 'SN', '產品類別', 'Remark']:  # 判断表格是否正确格式

                    # 判斷表格中是否有重複信息
                    if str(df.loc[i, 'SN'].replace(' ', '')) not in sn:

                        # 判断表格信息是否正确
                        for project_id in list(Project.objects.all().values_list("id", "pname")):
                            if df.loc[i, '專案'].replace(' ', '') in project_id:

                                # 专案正确, 获取对应专案id
                                fk_project_id = project_id[0]

                                for stage_id in list(Stage.objects.all().values_list("id", "sname", "fk_project_id")):

                                    if fk_project_id in stage_id and df.loc[i, '階段'].replace(' ', '') in stage_id:
                                        fk_stage_id = stage_id[0]
                                        break
                                    else:
                                        fk_stage_id = 0

                                break

                            else:
                                fk_project_id = 0

                        # ----------------------- Forest add

                        # 判断 产品类别
                        for pt_id in list(ProductType.objects.all().values_list("id", "ptname")):
                            if str(df.loc[i, '產品類別'].replace(' ', '')).lower() in pt_id[1].lower():
                                # 产品类别正确，获取其id
                                fk_pt_id = pt_id[0]
                                break
                            else:
                                fk_pt_id = 0
                        # -----------------------

                        if fk_project_id != 0 and fk_stage_id != 0 and fk_pt_id != 0:  # 专案阶段无误

                            msg = "上傳成功"
                            correct_unit.append(df.loc[i].tolist())  # 成功上传的项

                            inventory = Inventory()

                            inventory.recuser = request.user.name  # 入库者
                            inventory.fk_structure = request.user.department  # 入库部门
                            inventory.currRecUser = request.user.name
                            inventory.currRecDate = datetime.now()

                            inventory.fk_project_id = fk_project_id
                            inventory.fk_stage_id = fk_stage_id
                            inventory.rel = df.loc[i, '編號'].replace(' ', '')
                            inventory.sn = str(df.loc[i, 'SN'])
                            inventory.state = 1
                            inventory.remark = df.loc[i, 'Remark']

                            # 加入产品类别
                            inventory.fk_pt_id = fk_pt_id

                            inventory.save()
                        else:
                            msg = "機台信息有誤"
                            error_unit.append(df.loc[i].tolist())  # 信息有误的项
                    else:
                        msg = "機台重复机台"
                        repeat_unit.append(df.loc[i].tolist())  # 重複機台
                else:
                    msg = "表格格式有誤"
        else:
            msg = "請上傳表格文件"

        return render(request, 'dqe/Inventory/Inventory_upload_info.html',
                      {"msg": msg, "error_unit": error_unit, "correct_unit": correct_unit, "repeat_unit": repeat_unit})


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++==
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++==


# 庫存列表
class InventoryListView(LoginRequiredMixin, View):
    def get(self, request):

        fields = ['id', 'fk_project__pname', 'fk_stage__sname', 'rel', 'sn', 'indate', 'recuser', 'state',
                  'fk_structure__name', 'remark', 'currRecUser', 'currRecDate', 'fk_pt__ptname', 'fk_pt__id']
        searchFields = ['fk_project_id', 'fk_stage_id', 'sn', 'fk_pt_id']  # 与数据库字段一致 'fk_structure_id', 'indate'
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   i not in ['fk_project_id', 'fk_stage_id', 'fk_structure_id',
                             'fk_pt_id']}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
        # 通过id筛选数据，id必须是确定的，如果id不存在，那么不将该条件放入
        if request.GET.get('fk_project_id'):
            filters['fk_project_id'] = request.GET.get('fk_project_id')
        if request.GET.get('fk_stage_id'):
            filters['fk_stage_id'] = request.GET.get('fk_stage_id')
        if request.GET.get('fk_structure_id'):
            filters['fk_structure_id'] = request.GET.get('fk_structure_id')
        if request.GET.get('fk_pt_id'):
            filters['fk_pt_id'] = request.GET.get('fk_pt_id')
        # else:
        #     filters['fk_structure_id'] = request.user.department   进去只看到当前部门库存

        # 用于处理Rel编号
        if request.GET.get('relStart') and request.GET.get('relEnd'):
            filters['rel__icontains'] = request.GET.get('relEnd').split('-')[0]
            # 将查询范围内的库存id找出来
            invIds = []
            invObjs = Inventory.objects.all()
            for invObj in invObjs:
                if int(invObj.rel.split('-')[1]) >= int(request.GET.get('relStart').split('-')[1]) and int(
                        invObj.rel.split('-')[1]) <= int(request.GET.get('relEnd').split('-')[1]):
                    invIds.append(invObj.id)
            filters['id__in'] = invIds

        elif request.GET.get('relStart'):
            filters['rel__icontains'] = request.GET.get('relStart').split('-')[0]

            invObjs = Inventory.objects.all()
            invIds = []
            for invObj in invObjs:
                if int(invObj.rel.split('-')[1]) >= int(request.GET.get('relStart').split('-')[1]):
                    invIds.append(invObj.id)
            filters['id__in'] = invIds

        elif request.GET.get('relEnd'):
            filters['rel__icontains'] = request.GET.get('relEnd').split('-')[0]
            invObjs = Inventory.objects.all()
            invIds = []
            for invObj in invObjs:
                if int(invObj.rel.split('-')[1]) >= int(request.GET.get('relStart').split('-')[1]):
                    invIds.append(invObj.id)
            filters['id__in'] = invIds
        else:
            pass

        # 查找出操作缓存表的记录 OperateCacheTable,目的,将一个人已经填单的
        # octObjs = OperateCacheTable.objects.filter(opeuser=request.user.name).values()
        # print(octObjs)
        # invobj = Inventory.objects.filter(operatecachetable__isnull=False).values_list('operatecachetable__opeuser', 'currRecUser')

        # 查询Inventory所有结果
        # res = dict(data=list(Inventory.objects.values(*fields)))
        # res = dict(data=list(Inventory.objects.filter(**filters).values(*fields).order_by('-indate')))

        res = dict(data=list(
            Inventory.objects.filter(**filters).values(*fields, 'operatecachetable__opeuser').order_by('-indate'))[
                        :500])
        # res = dict()
        # res['data'] = list(Inventory.objects.filter(**filters).values(*fields).order_by('-indate'))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 庫存 新增 和 修改
# get方式是跳转链接，而post方式是submit
class InventoryUpdateView(LoginRequiredMixin, View):
    # 注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):
        res = dict()

        if 'id' in request.GET and request.GET['id']:
            inventory = get_object_or_404(Inventory, pk=request.GET.get('id'))
            res['inventory'] = inventory
        else:
            inventorys = Inventory.objects.all()
            res['inventorys'] = inventorys

        # 狀態
        state_list = []
        for state in Inventory.STATE_TYPE:
            state_dict = dict(key=state[0], value=state[1])
            state_list.append(state_dict)

        res['state_list'] = state_list

        # 專案
        projects = Project.objects.all()
        res['projects'] = projects

        # 階段
        stages = Stage.objects.all()
        res['stages'] = stages

        # 部門
        structures = Structure.objects.all()
        res['structures'] = structures

        # 產品類型
        prodtypes = ProductType.objects.all()
        res['prodtypes'] = prodtypes

        return render(request, 'dqe/Inventory/Inventory_Update.html', res)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:  # id的存在，就是为了说明是新增数据还是编辑数据
            inventory = get_object_or_404(Inventory, pk=request.POST.get('id'))
        else:
            inventory = Inventory()
            # inventory.indate 入库时间
            inventory.recuser = request.user.name
            inventory.fk_structure = request.user.department
            inventory.currRecUser = request.user.name
            inventory.currRecDate = datetime.now()

        inventory_create_form = InventoryCreateForm(request.POST, instance=inventory)
        if inventory_create_form.is_valid():
            inventory_create_form.save()

            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 库存删除
class InventoryDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            Inventory.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 庫存機台出庫操作
class InventoryOutView(LoginRequiredMixin, View):
    def post(self, request):
        print("++++++++++++++++++++")
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            list_inventory = Inventory.objects.filter(id__in=id_list)
            for i_list_inventory in list_inventory:
                i_list_inventory.state = '4'
                i_list_inventory.save()
                print("更改成功！！！")
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 庫存機台入库操作
class InventoryInView(LoginRequiredMixin, View):
    def post(self, request):
        # fk_structure__name
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            list_inventory = Inventory.objects.filter(id__in=id_list)
            for i_list_inventory in list_inventory:
                i_list_inventory.state = '1'
                i_list_inventory.currRecUser = request.user.name
                i_list_inventory.fk_structure_id = request.user.department.id
                i_list_inventory.save()
                print("更改成功！！！")
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 将要申请的机台放入操作缓冲表 OperateCacheTable
class InventoryAddToShoppingView(LoginRequiredMixin, View):

    def post(self, request):
        res = dict(result=False)

        # 将该机台的id和申请人对应的id 存入到操作缓存表OperateCacheTable
        # 只支持 保存的用户，团队才能查看

        try:
            if request.user.department:  # 可能没登录，就获取不到
                # octObj = OperateCacheTable()
                # octObj.fk_inventory = Inventory.objects.get(id=request.POST.get("id"))
                # octObj.fk_structure = Structure.objects.get(name=request.user.department)
                # octObj.save()
                # 设定规则，同一用户，一次不能多次勾选该机台
                OperateCacheTable.objects.get_or_create(
                    fk_inventory=Inventory.objects.get(id=request.POST.get("id")),
                    fk_structure=Structure.objects.get(name=request.user.department),
                    opeuser=request.user.name
                )

                res['result'] = True
        except:
            res['result'] = False  # 前台彈出 添加失敗,請重新添加！

        return HttpResponse(json.dumps(res), content_type='application/json')


# 历史详细
class InventoryDetailView(LoginRequiredMixin, View):
    def get(self, request):
        temp_id = request.GET.get('inventoryId')

        # res = dict(data=Inventory.objects.all())
        res = dict(apply=Inventory.objects.get(id=int(temp_id)))  # 獲取倉庫的信息   apply應該是inventory

        # 思路
        # 1.原始数据 : 查找Apply 和 ApplyDetail 中 fk_Inventory_id == 传递过来的id, 根据机台申请前状态，查找出该机台的原始数据

        fields = ['id', 'fk_inventory__fk_project__pname', 'fk_inventory__fk_stage__sname', 'fk_inventory__rel',
                  'fk_inventory__sn', 'indate', 'recuser', 'state', 'fk_structure__name', 'remark', 'currRecUser',
                  'currRecDate'
                  ]
        filters = {}
        # res['oridata'] = list(ApplyDetail.objects.filter(**filters).values(*fields, 'operatecachetable__opeuser').order_by('-indate'))

        # 2.当前数据 : 遍历Inventory即为当前数据

        # 3.历史数据 : 查找出Apply 和 ApplyDetail中所有 fk_inventory_id == 传递过来id的就可以。 这里可以独立出一个函数InventoryDetailListView

        now_time = datetime.now()
        lt = now_time - datetime.strptime(res['apply'].currRecDate, '%Y-%m-%d %H:%M:%S.%f')
        res['apply'].stayTime = str(lt.days) + "D" + " " + str(floor(lt.seconds / 60 / 60)) + "H"
        res['apply'].currRecDate = datetime.strptime(res['apply'].currRecDate, '%Y-%m-%d %H:%M:%S.%f')

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)

        return render(request, 'dqe/Inventory/Inventory_Detail.html', res)


# 机台历史数据
class InventoryDetailListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['fk_apply__applyNum', 'fk_apply__applyUser', 'fk_apply__applyUnit', 'fk_apply__applyDate',
                  'fk_apply__applyTime', 'fk_apply__applyState', 'confirmUser', 'machineState',
                  'lendDate', 'lendUnit', 'lendtime', 'remark', 'macAppState']
        # searchFields = ['applyDate', 'lendDate', 'applyUnit', 'lendUnit', 'applyUser', 'applyState']  # 与数据库字段一致
        # filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
        #            i not in [''] and request.GET.get(i, '')}

        res = dict(data=list(
            ApplyDetail.objects.filter(fk_inventory_id=int(request.GET.get('applyId'))).values(*fields).order_by(
                '-fk_apply__applyDate')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 扫码 申请
class InventoryScanApplyView(LoginRequiredMixin, View):
    # 注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
    def get(self, request):
        res = dict()
        return render(request, 'dqe/Inventory/ScanApply.html', res)

    def post(self, request):

        res = dict(result=False)

        sns = request.POST.get('sns').split('\r\n')
        # 思路：分两步 a.如果该sn存在库存中，那么将相应的Inventory_ID放入 OperateCacheTable 表中
        #          b.如果sn未在库存中找到，那么就将未找到的sn回应给客户

        # STATE_TYPE = (("1", "入庫"), ("2", "可申請"), ("3", "被申請"), ("4", "出库"))

        invState2SN = []  # 库存状态为已经借出的SN
        invState3SN = []  # 库存状态为被申请的SN
        invState4SN = []  # 库存状态为已出库的SN
        invNotSN = []  # 将扫码没有的机台存放
        try:
            if request.user.department:  # 可能没登录，就获取不到
                for sn in sns:
                    invObj = Inventory.objects.filter(sn=sn)
                    print(invObj)
                    # 判断对象是否存在，不存在表示该sn库存中没有
                    if invObj:
                        # 如果有对象 , 已经借出的、被申请、出库的不能进入缓存中，并提示相应信息
                        if invObj[0].state != '3' and invObj[0].state != '4' and invObj[0].state != '2':
                            OperateCacheTable.objects.get_or_create(
                                fk_inventory=invObj[0],
                                fk_structure=Structure.objects.get(name=request.user.department),
                                opeuser=request.user.name
                            )
                        else:
                            if invObj[0].state == '3':
                                invState3SN.append(sn)  # 将被申请的sn归纳出来
                            elif invObj[0].state == '4':
                                invState4SN.append(sn)  # 将出库的sn归纳出来
                            elif invObj[0].state == '2':
                                invState2SN.append(sn)  # 将已经借出的机台的sn归纳出来
                            else:
                                pass
                    else:
                        invNotSN.append(sn)
            print(invState2SN)
            # 如果没有出现以下3种情况 則為1   # 1 表成功  2 表部分成功  3异常
            if invState3SN or invState4SN or invNotSN or invState2SN:
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
            # print(e)
            res['result'] = 3
        print(res)
        return HttpResponse(json.dumps(res), content_type='application/json')


class InventoryScanReturnView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dqe/Inventory/ScanReturn.html', None)

    def post(self, request):
        pass
