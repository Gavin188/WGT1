# import json
# from datetime import datetime
# from math import floor
# import re
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
# from dqe.models import Inventory, Project, Stage, OperateCacheTable, RecordTable, ProductType
# from system.mixin import LoginRequiredMixin
# from system.models import Structure,Menu
# #庫存界面
# #@method_decorator(login_required, name='dispatch') #测试3
# class OutdateWarnView(LoginRequiredMixin, View):
#     def get(self, request):
#         res = dict(data=Inventory.objects.all())
#         # 專案
#         projects = Project.objects.all()
#         res['projects'] = projects
#
#         # 階段
#         stages = Stage.objects.all()
#         res['stages'] = stages
#
#         # 部門
#         structures = Structure.objects.all()
#         res['structures'] = structures
#
#         # 產品類型
#         prodtypes = ProductType.objects.all()
#         res['prodtypes'] = prodtypes
#
#         menu = Menu.get_menu_by_request_url(url=self.request.path_info)
#         if menu is not None:
#             res.update(menu)
#
#
#         return render(request, 'dqe/OutdateWarn/OutdateWarn_List.html',res)
#
# #庫存列表，在各个部门下停留的时间统计
# class OutdateWarnListView(LoginRequiredMixin, View):
#     def get(self, request):
#
#         fields = ['id', 'fk_project__pname', 'fk_stage__sname', 'rel','sn','indate','recuser','state','fk_structure__name','remark','currRecUser','currRecDate','fk_pt__ptname']
#         searchFields = ['fk_project_id', 'fk_stage_id', 'sn'] #与数据库字段一致 'fk_structure_id', 'indate'
#         filters = {i + '__icontains': request.GET.get(i,'') for i in searchFields if i not in ['fk_project_id','fk_stage_id','fk_structure_id',]}  #此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
#
#         #通过id筛选数据，id必须是确定的，如果id不存在，那么不将该条件放入
#         if request.GET.get('fk_project_id'):
#             filters['fk_project_id'] = request.GET.get('fk_project_id')
#         if request.GET.get('fk_stage_id'):
#             filters['fk_stage_id'] = request.GET.get('fk_stage_id')
#         if request.GET.get('fk_structure_id'):
#             filters['fk_structure_id'] = request.GET.get('fk_structure_id')
#         if request.GET.get('fk_pt_id'):
#             filters['fk_pt_id'] = request.GET.get('fk_pt_id')
#
#         #用于处理Rel编号
#         if request.GET.get('relStart') and request.GET.get('relEnd') :
#             filters['rel__icontains'] = request.GET.get('relEnd').split('-')[0]
#             #将查询范围内的库存id找出来
#             invIds = []
#             invObjs = Inventory.objects.all()
#             for invObj in invObjs:
#                 if int(invObj.rel.split('-')[1]) >= int(request.GET.get('relStart').split('-')[1]) and int(invObj.rel.split('-')[1]) <= int(request.GET.get('relEnd').split('-')[1]):
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
#         #查找出操作缓存表的记录 OperateCacheTable,目的,将一个人已经填单的
#         #octObjs = OperateCacheTable.objects.filter(opeuser=request.user.name).values()
#         #print(octObjs)
#         #invobj = Inventory.objects.filter(operatecachetable__isnull=False).values_list('operatecachetable__opeuser', 'currRecUser')
#
#         #查询Inventory所有结果
#         #res = dict(data=list(Inventory.objects.values(*fields)))
#         #res = dict(data=list(Inventory.objects.filter(**filters).values(*fields).order_by('-indate')))
#
#         list_data = list(Inventory.objects.filter(**filters).values(*fields,'operatecachetable__opeuser').order_by('-indate'))[:500]
#         now_time = datetime.now()
#         for i_list_data in list_data:
#             #print(i_list_data)
#             list_record = RecordTable.objects.filter(fk_inventory=i_list_data['id'])
#             #print(list_record)
#             index = list_data.index(i_list_data)  # 该dic在list中索引值
#             if list_record:#不为空的情况，即有累计的时间记录
#                 for i_list_record in list_record:#遍历查询出来的部门信息和时间累计表
#                     # lt = now_time - datetime.strptime(list_data[index]["currRecDate"], '%Y-%m-%d %H:%M:%S.%f')
#                     # list_D_H = re.findall(r'\d+', i_list_record.stayTimeTotal)  # 第一个数字为D，第二个数字为H  ﻿['1', '22']
#                     # new_record_time = str(int(lt.days) + int(list_D_H[0])) + "D" + " " + str(int(floor(lt.seconds / 60 / 60)) + int(list_D_H[1])) + "H"
#                     # list_data[index][i_list_record.fk_structure.name] = new_record_time  # 若是存在时间累加记录的，key值为部门名称，value值为累计时长
#                     list_data[index][i_list_record.fk_structure.name] = i_list_record.stayTimeTotal
#                     if i_list_data['fk_structure__name'] == i_list_record.fk_structure.name: #以前存在过停留记录，但同时机台又在本部门
#                         lt = now_time - datetime.strptime(list_data[index]["currRecDate"], '%Y-%m-%d %H:%M:%S.%f')
#                         list_D_H = re.findall(r'\d+', i_list_record.stayTimeTotal)  # 第一个数字为D，第二个数字为H  ﻿['1', '22']
#                         new_record_time = str(int(lt.days) + int(list_D_H[0])) + "D" + " " + str(
#                             int(floor(lt.seconds / 60 / 60)) + int(list_D_H[1])) + "H"
#                         list_data[index][i_list_record.fk_structure.name] = new_record_time  # 若是存在时间累加记录的，key值为部门名称，value值为累计时长
#
#             result_str_name = list_data[index]['fk_structure__name']  #查詢當前部門的名稱
#             if 'FA' not in list_data[index].keys():    #機台從來沒有在FA停留過
#                 if result_str_name == "FA":
#                     lt = now_time - datetime.strptime(list_data[index]["currRecDate"], '%Y-%m-%d %H:%M:%S.%f')
#                     list_data[index]["FA"] = str(lt.days) + "D" + " " + str(floor(lt.seconds / 60 / 60)) + "H"
#                 else:
#                     list_data[index]["FA"] = "0D 0H"
#             # elif 'FA' in list_data[index].keys() and result_str_name == 'FA':  #以前FA借過該機台，並且該機台存在FA部門
#             #     lt = now_time - datetime.strptime(list_data[index]["currRecDate"], '%Y-%m-%d %H:%M:%S.%f')
#             #     list_D_H = re.findall(r'\d+', i_list_record.stayTimeTotal)  # 第一个数字为D，第二个数字为H  ﻿['1', '22']
#             #     new_record_time = str(int(lt.days) + int(list_D_H[0])) + "D" + " " + str(int(floor(lt.seconds / 60 / 60)) + int(list_D_H[1])) + "H"
#             #     list_data[index][result_str_name] = new_record_time  # 若是存在时间累加记录的，key值为部门名称，value值为累计时长
#
#
#             if 'MiniLine' not in list_data[index].keys():
#                 if result_str_name == "MiniLine":
#                     lt = now_time - datetime.strptime(list_data[index]["currRecDate"], '%Y-%m-%d %H:%M:%S.%f')
#                     list_data[index]["MiniLine"] = str(lt.days) + "D" + " " + str(floor(lt.seconds / 60 / 60)) + "H"
#                 else:
#                     list_data[index]["MiniLine"] = "0D 0H"
#
#             if 'EQU' not in list_data[index].keys():
#                 if result_str_name == "EQU":
#                     lt = now_time - datetime.strptime(list_data[index]["currRecDate"], '%Y-%m-%d %H:%M:%S.%f')
#                     list_data[index]["EQU"] = str(lt.days) + "D" + " " + str(floor(lt.seconds / 60 / 60)) + "H"
#                 else:
#                     list_data[index]["EQU"] = "0D 0H"
#
#             if 'PM' not in list_data[index].keys():
#                 if result_str_name == "PM":
#                     lt = now_time - datetime.strptime(list_data[index]["currRecDate"], '%Y-%m-%d %H:%M:%S.%f')
#                     list_data[index]["PM"] = str(lt.days) + "D" + " " + str(floor(lt.seconds / 60 / 60)) + "H"
#                 else:
#                     list_data[index]["PM"] = "0D 0H"
#
#
#         res = dict(data=list_data)
#
#         #res['data'] = list(Inventory.objects.filter(**filters).values(*fields).order_by('-indate'))
#
#         return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
#
#
