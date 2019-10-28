# import json
# from math import floor
# from datetime import datetime
# from django.contrib.auth.decorators import login_required
# from django.db.models import Q
# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
# from django.utils.decorators import method_decorator
# from django.views.generic.base import View
# from django.http import HttpResponse
# from django.core.serializers.json import DjangoJSONEncoder
#
# from custom import BreadcrumbMixin
# from dqe.forms import InventoryCreateForm
# from dqe.models import Inventory, Project, Stage, OperateCacheTable, ApplyDetail, Apply, ProductType, ResetHistory
# from system.mixin import LoginRequiredMixin
# from system.models import Structure, Menu
#
#
# 庫存界面
# @method_decorator(login_required, name='dispatch') #测试3
from django.shortcuts import render
from django.views import View

from system.mixin import LoginRequiredMixin
from system.models import Menu
#
#
# class MachineStatusQueryView(LoginRequiredMixin, View):
#
#     def get(self, request):
#         res = {}
#         # menu = Menu.get_menu_by_request_url(url=self.request.path_info)
#         # print(menu)
#         # if menu is not None:
#         #     res.update(menu)
#
#         return render(request, 'overtime/Abnormal/abnormalist.html', res)


# # 异常申请
# class AbnormalListView(LoginRequiredMixin, View):
#     def get(self, request):
#         res = {}
#         menu = Menu.get_menu_by_request_url(url=self.request.path_info)
#         print(menu)
#         if menu is not None:
#             res.update(menu)
#         return render(request, 'overtime/Abnormal/abnormalist.html', res)
#
# #
#
# # 庫存列表
# class MachineStatusQueryListView(LoginRequiredMixin, View):
#     def get(self, request):
#
#         fields = ['id', 'fk_project__pname', 'fk_stage__sname', 'rel', 'sn', 'indate', 'recuser', 'state',
#                   'fk_structure__name', 'remark', 'currRecUser', 'currRecDate', 'fk_pt__ptname', ]
#         searchFields = ['fk_project_id', 'fk_stage_id', 'sn']  # 与数据库字段一致 'fk_structure_id', 'indate'
#         filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
#                    i not in ['fk_project_id', 'fk_stage_id',
#                              'fk_structure_id', ]}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
#
#         # 通过id筛选数据，id必须是确定的，如果id不存在，那么不将该条件放入
#         if request.GET.get('fk_project_id'):
#             filters['fk_project_id'] = request.GET.get('fk_project_id')
#         if request.GET.get('fk_stage_id'):
#             filters['fk_stage_id'] = request.GET.get('fk_stage_id')
#         if request.GET.get('fk_structure_id'):
#             filters['fk_structure_id'] = request.GET.get('fk_structure_id')
#         if request.GET.get('fk_pt_id'):
#             filters['fk_pt_id'] = request.GET.get('fk_pt_id')
#
#         # 用于处理Rel编号
#         if request.GET.get('relStart') and request.GET.get('relEnd'):
#             filters['rel__icontains'] = request.GET.get('relEnd').split('-')[0]
#             # 将查询范围内的库存id找出来
#             invIds = []
#             invObjs = Inventory.objects.all()
#             for invObj in invObjs:
#                 if int(invObj.rel.split('-')[1]) >= int(request.GET.get('relStart').split('-')[1]) and int(
#                         invObj.rel.split('-')[1]) <= int(request.GET.get('relEnd').split('-')[1]):
#                     invIds.append(invObj.id)
#             filters['id__in'] = invIds
#
#         elif request.GET.get('relStart'):
#             filters['rel__icontains'] = request.GET.get('relStart').split('-')[0]
#
#             invObjs = Inventory.objects.all()
#             invIds = []
#             for invObj in invObjs:
#                 if int(invObj.rel.split('-')[1]) >= int(request.GET.get('relStart').split('-')[1]):
#                     invIds.append(invObj.id)
#             filters['id__in'] = invIds
#
#         elif request.GET.get('relEnd'):
#             filters['rel__icontains'] = request.GET.get('relEnd').split('-')[0]
#             invObjs = Inventory.objects.all()
#             invIds = []
#             for invObj in invObjs:
#                 if int(invObj.rel.split('-')[1]) >= int(request.GET.get('relStart').split('-')[1]):
#                     invIds.append(invObj.id)
#             filters['id__in'] = invIds
#         else:
#             pass
#
#         res = dict(data=list(
#             Inventory.objects.filter(**filters).values(*fields, 'operatecachetable__opeuser').order_by('-indate'))[
#                         :500])
#         print(res)
#         return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
#
#
# # 机台状态查询详情
# class MachineStatusQueryDetailView(LoginRequiredMixin, View):
#
#     def get(self, request):
#         temp_id = request.GET.get('inventoryId')
#
#         # res = dict(data=Inventory.objects.all())
#         res = dict(apply=Inventory.objects.get(id=int(temp_id)))  # 獲取倉庫的信息   apply應該是inventory
#         # 思路
#         # 1.原始数据 : 查找Apply 和 ApplyDetail 中 fk_Inventory_id == 传递过来的id, 根据机台申请前状态，查找出该机台的原始数据
#
#         fields = ['id', 'fk_inventory__fk_project__pname', 'fk_inventory__fk_stage__sname', 'fk_inventory__rel',
#                   'fk_inventory__sn', 'indate', 'recuser', 'state', 'fk_structure__name', 'remark', 'currRecUser',
#                   'currRecDate'
#                   ]
#         filters = {}
#         # res['oridata'] = list(ApplyDetail.objects.filter(**filters).values(*fields, 'operatecachetable__opeuser').order_by('-indate'))
#
#         # 2.当前数据 : 遍历Inventory即为当前数据
#
#         # 3.历史数据 : 查找出Apply 和 ApplyDetail中所有 fk_inventory_id == 传递过来id的就可以。 这里可以独立出一个函数MachineStatusQueryDetailListView
#
#         # menu = Menu.get_menu_by_request_url(url=self.request.path_info)
#         # if menu is not None:
#         #     res.update(menu)
#         now_time = datetime.now()
#         lt = now_time - datetime.strptime(res['apply'].currRecDate, '%Y-%m-%d %H:%M:%S.%f')
#         res['apply'].stayTime = str(lt.days) + "D" + " " + str(floor(lt.seconds / 60 / 60)) + "H"
#
#         res['apply'].currRecDate = datetime.strptime(res['apply'].currRecDate, '%Y-%m-%d %H:%M:%S.%f')
#
#         return render(request, 'dqe/MachineStatusQuery/MachineStatusQuery_Detail.html', res)
#
#
# # 机台状态查询详情：列表
# # 3.历史数据
# class MachineStatusQueryDetailListView(LoginRequiredMixin, View):
#     def get(self, request):
#         fields = ['fk_apply__applyNum', 'fk_apply__applyUser', 'fk_apply__applyUnit', 'fk_apply__applyDate',
#                   'fk_apply__applyTime', 'fk_apply__applyState', 'confirmUser', 'machineState',
#                   'lendDate', 'lendUnit', 'lendtime', 'remark']
#         # searchFields = ['applyDate', 'lendDate', 'applyUnit', 'lendUnit', 'applyUser', 'applyState']  # 与数据库字段一致
#         # filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
#         #            i not in [''] and request.GET.get(i, '')}
#
#         res = dict(data=list(
#             ApplyDetail.objects.filter(fk_inventory_id=int(request.GET.get('applyId'))).values(*fields).order_by(
#                 '-fk_apply__applyDate')))
#
#         return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
#
#
# # 4. Reset数据
# # MachineStatusQueryResetListView
# class MachineStatusQueryResetListView(LoginRequiredMixin, View):
#
#     def get(self, request):
#         fields = ['fk_inv__rel', 'resetUser', 'resetDept', 'resetTime', 'resetRemark']
#         # searchFields = ['applyDate', 'lendDate', 'applyUnit', 'lendUnit', 'applyUser', 'applyState']  # 与数据库字段一致
#         # filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
#         #            i not in [''] and request.GET.get(i, '')}
#
#         res = dict(data=list(
#             ResetHistory.objects.filter(fk_inv_id=int(request.GET.get('applyId'))).values(*fields).order_by(
#                 '-resetTime')))
#
#         return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
