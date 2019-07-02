import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from custom import BreadcrumbMixin
from dqe.forms import OperateCacheTableCreateForm
from dqe.models import OperateCacheTable, Project, Stage, Apply, Inventory, ApplyDetail
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu

import datetime


# 操作緩存 界面
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


# 操作緩存 列表
class OperateCacheTableListView(LoginRequiredMixin, View):
    def get(self, request):

        fields = ['id', 'fk_inventory__id', 'fk_structure__id', 'fk_inventory__fk_project__pname',
                  'fk_inventory__fk_stage__sname', 'fk_inventory__rel', 'fk_inventory__sn', 'fk_inventory__indate',
                  'fk_inventory__state', 'fk_inventory__fk_structure__name', 'fk_structure__name',
                  'fk_inventory__recuser',
                  'fk_inventory__currRecUser', 'opeuser', 'fk_inventory__currRecDate'
                  ]
        searchFields = ['fk_project_id', 'fk_stage_id', 'fk_structure_id', ]  # 与数据库字段一致 # 'fk_inventory__rel',
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   i not in ['fk_project_id', 'fk_stage_id',
                             'fk_structure_id', ]}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        print(request.GET.get(i) for i in searchFields)

        # __icontains 忽略大小写
        # 通过id筛选数据，id必须是确定的，如果id不存在，那么不将该条件放入
        if request.GET.get('fk_project_id'):
            filters['fk_inventory__fk_project__id'] = request.GET.get('fk_project_id')
        if request.GET.get('fk_stage_id'):
            filters['fk_inventory__fk_stage__id'] = request.GET.get('fk_stage_id')
        if request.GET.get('fk_structure_id'):
            filters['fk_structure_id'] = request.GET.get('fk_structure_id')
        else:  # 此处应该以部门的方式遍历 该操作缓存表
            filters['fk_structure'] = Structure.objects.get(name=request.user.department)

        # 用于处理Rel编号
        if request.GET.get('relStart') and request.GET.get('relEnd'):
            filters['fk_inventory__rel__icontains'] = request.GET.get('relEnd').split('-')[0]
            # 将查询范围内的库存id找出来
            invIds = []
            invObjs = Inventory.objects.all()
            for invObj in invObjs:
                if int(invObj.rel.split('-')[1]) >= int(request.GET.get('relStart').split('-')[1]) and int(
                        invObj.rel.split('-')[1]) <= int(request.GET.get('relEnd').split('-')[1]):
                    invIds.append(invObj.id)
            filters['fk_inventory__id__in'] = invIds

        elif request.GET.get('relStart'):
            filters['fk_inventory__rel__icontains'] = request.GET.get('relStart').split('-')[0]

            invObjs = Inventory.objects.all()
            invIds = []
            for invObj in invObjs:
                if int(invObj.rel.split('-')[1]) >= int(request.GET.get('relStart').split('-')[1]):
                    invIds.append(invObj.id)
            filters['fk_inventory__id__in'] = invIds

        elif request.GET.get('relEnd'):
            filters['fk_inventory__rel__icontains'] = request.GET.get('relEnd').split('-')[0]
            invObjs = Inventory.objects.all()
            invIds = []
            for invObj in invObjs:
                if int(invObj.rel.split('-')[1]) >= int(request.GET.get('relStart').split('-')[1]):
                    invIds.append(invObj.id)
            filters['fk_inventory__id__in'] = invIds
        else:
            pass

        print('oper', filters)

        # 查询OperateCacheTable所有结果
        # res = dict(data=list(OperateCacheTable.objects.values(*fields)))
        res = dict(data=list(OperateCacheTable.objects.filter(**filters).values(*fields)))
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class OperateCacheTableUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict()

        if 'id' in request.GET and request.GET['id']:
            oct = get_object_or_404(OperateCacheTable, pk=request.GET.get('id'))
            res['oct'] = oct
        else:
            octs = OperateCacheTable.objects.all()
            res['octs'] = octs

        return render(request, 'dqe/OperateCacheTable/OperateCacheTable_Update.html', res)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:  # id的存在，就是为了说明是新增数据还是编辑数据
            oct = get_object_or_404(OperateCacheTable, pk=request.POST.get('id'))
        else:
            oct = OperateCacheTable()

        oct_create_form = OperateCacheTableCreateForm(request.POST, instance=oct)

        if oct_create_form.is_valid():
            oct_create_form.save()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 操作緩存表 删除操作
class OperateCacheTableDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = list(map(int, request.POST.get('id').split(',')))[0]
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            OperateCacheTable.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# 申请确认
# 思路：创建Apply>将ApplyDetail也创建出来>清空操作缓存>库存中的状态变为被申请状态
class ApplyConfirmView(LoginRequiredMixin, View):

    def post(self, request):
        print(request.POST.get('id').split(','))
        res = dict(result=False)

        if 'id' in request.POST and request.POST['id']:

            # 為创建单号做准备
            id = list(map(int, request.POST.get('id').split(',')))[0]
            print('id', id)
            octObj = OperateCacheTable.objects.get(id=id)
            print('oct', octObj)
            invObj0 = Inventory.objects.get(id=octObj.fk_inventory.id)
            print('inv', invObj0)

            # 创建一个申请单  申请单号设定为 申请部门 向 确认部门 申请时间
            apply = Apply()
            apply.applyNum = str(request.user.department) + "-" + str(invObj0.fk_structure.name) + "-" + str(
                datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
            apply.applyUser = request.user.username
            # apply.applyTime 申請時長-当确认后才可计算
            apply.applyUnit = request.user.department  # 申請單位
            apply.applyDate = datetime.datetime.now()
            apply.applyState = 1  # ("1", "待簽核"), ("2", "已簽核")
            apply.save()

            # 将操作缓存表中的数据 加入 到applydetail
            id_list = map(int, request.POST.get('id').split(','))
            print('id_list', id_list)
            octObjs = OperateCacheTable.objects.filter(id__in=id_list)
            print(octObjs)
            for oct in octObjs:
                ApplyDetail.objects.create(
                    fk_apply=apply,
                    fk_inventory=oct.fk_inventory,
                    # machineState= 默认为未确认
                    confirmUser=oct.fk_inventory.currRecUser,  # 机台确认人=库存當前接收人
                    # lendDate = 借出时间，确认时
                    lendUnit=oct.fk_inventory.fk_structure.name,
                    # lendtime = 借出时长，确认时加上
                    # remark = 借出时 加上
                    macAppState=oct.fk_inventory.state  # 借出前的状态/機台申請前狀態
                )

                # 申请提单时，改变库存中的状态 变为被申请即可，当确认该单时，那么当前使用部门、当前入库人、当前入库日期都要改
                oct.fk_inventory.state = 3  # ("1", "入庫"), ("2", "可申請"), ("3", "被申請"), ("4", "出库")
                oct.fk_inventory.save()

            # 清空该操作缓存 ，因为此处是勾选出来的OperateCacheTable的id,所以不需要查找部门后在滤除
            octObjs.delete()

            res['result'] = True
        else:
            res['result'] = False

        return HttpResponse(json.dumps(res), content_type='application/json')
