import json
import re
from math import floor

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from custom import BreadcrumbMixin
from dqe.forms import ApplyCreateForm
from dqe.models import Apply, Project, Stage, ApplyDetail, RecordTable
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu
from datetime import datetime
from django.db.models import Count


# 借出确认 界面
class LoanConfirmView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=Apply.objects.all())

        # 部門
        structures = Structure.objects.all()
        res['structures'] = structures

        # 申請單狀態
        applyState_list = []
        for applyState in Apply.APPLYSTATE_TYPE:
            applyState_dict = dict(key=applyState[0], value=applyState[1])
            applyState_list.append(applyState_dict)
        res['applyState_list'] = applyState_list

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)

        return render(request, 'dqe/LoanConfirm/LoanConfirm_List.html', res)


# 借出确认 列表
class LoanConfirmListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'applyNum', 'applyUser', 'applyDate', 'applyUnit', 'applyTime', 'applyState', 'lendRemark']
        searchFields = ['applyDate', 'applyUnit', 'applyUser', 'applyState']  # 与数据库字段一致
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   i not in ['', ] and request.GET.get(i,
                                                       '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        # 假如时间采用区间的方式，用如下方式进行处理  时间格式转化 datetime.datetime.strptime(request.GET.get('StartDate'), "%m/%d/%Y")
        # if request.GET.get('startapplyDate'):
        #     filters['applyDate__gte'] = request.GET.get('startapplyDate')
        # if request.GET.get('endapplyDate'):
        #     filters['applyDate__lte'] = request.GET.get('endapplyDate')

        # 借出确认： 筛选出借出部门所要签的单。1. 根据Apply中的 申请状态排序 。 2. 通过ApplyDetail中的借出单位，反向找出Apply的Id,然后再将Apply中的所有单显示出来。
        # 注意：不管该部门根据条件遍历，遍历的都是该部门的数据
        applyDetailObjs = ApplyDetail.objects.filter(lendUnit=request.user.department)
        adlists = [i.fk_apply.id for i in applyDetailObjs]
        alists = list(set(adlists))
        filters['id__in'] = alists

        res = dict(data=list(Apply.objects.filter(**filters).values(*fields).order_by('applyState')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 进入申請單詳情界面
class LoanConfirmDetailView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            apply = get_object_or_404(Apply, pk=request.GET.get('id'))
        ret['apply'] = apply

        return render(request, 'dqe/LoanConfirm/LoanConfirm_Detail.html', ret)


# 申请详情列表
class LoanConfirmDetailListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'fk_inventory__fk_project__pname', 'fk_inventory__fk_stage__sname', 'fk_inventory__rel',
                  'fk_inventory__sn', 'fk_apply__applyNum', 'fk_apply__applyUser', 'fk_apply__applyUnit',
                  'fk_apply__applyDate', 'machineState',
                  'lendUnit', 'confirmUser', 'lendDate', 'remark', 'macAppState', 'lendtime']
        searchFields = ['fk_inventory__rel', 'machineState', ]  # 查询条件
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        filters['fk_apply_id'] = request.GET.get("applyId")

        res = dict(data=list(ApplyDetail.objects.filter(**filters).values(*fields).order_by('-fk_apply__applyDate')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 進入申請單備註 編輯界面
# 思路：LoanConfirm_List.html > views_loanconfirm.py(GET) > ApplyRemark.html > views_loanconfirm.py(POST)
class LoanConfirmAremarkView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        # 同时确认多个单，需要传递多个单的applyId
        # id_list = map(int, request.POST.get('applyId').split(','))
        ret['applyIds'] = request.GET.get('applyIds')

        return render(request, 'dqe/LoanConfirm/ApplyRemark.html', ret)

    # 一次確認一個單或一次確認多個單
    def post(self, request):
        res = dict(result=False)

        # 思路：获取到ApplyID > 循环遍历ApplyDetail >
        # > 将applydetail中的 借出時長、機台確認狀態、Remark為''、借出日期 > 【借出时长，用于记录机台记录上一次历史的信息】
        # > 接着更新Apply单中的数据（申请时长，申请单状态，申请单备注，） >
        # > 最后，申请单信息改完，那么就是 库存表 当前使用部门、当前部门停留时间、当前入库接收者、当前入库接收时间、状态
        # > 更改完成之后，一个申请流程结束， 进入机台状况查询。。

        if 'arrlyIds' in request.POST and request.POST['arrlyIds']:
            id_list = map(int, request.POST.get('arrlyIds').split(','))
            print('1111111111', id_list)
            applyObjs = Apply.objects.filter(id__in=id_list)
            print('222222222', applyObjs)
            # 遍历整个ApplyDetail
            for applyObj in applyObjs:

                # 更新Apply表中的数据
                at = datetime.now() - applyObj.applyDate
                applyObj.applyTime = str(at.days) + "D" + " " + str(
                    floor(at.seconds / 60 / 60)) + "H"  # 申请时长 = 确认日期（当前确认的时间） - 申请日期
                applyObj.applyState = 2  # ("1", "待簽核"), ("2", "已簽核"),
                applyObj.lendRemark = request.POST.get("lendRemark")
                applyObj.save()

                adobjs = ApplyDetail.objects.filter(fk_apply=applyObj)  # 状态：("1", "未確認"), ("2", "確認"), ("3", "拒絕"),

                for adobj in adobjs:
                    adobj.lendDate = datetime.now()
                    # 字符串时间格式转化
                    lt = adobj.lendDate - datetime.strptime(adobj.fk_inventory.currRecDate,
                                                            '%Y-%m-%d %H:%M:%S.%f')  # 借出时长 = 借出日期 - 机台当前入库时间  历史
                    adobj.lendtime = str(lt.days) + "D" + " " + str(floor(lt.seconds / 60 / 60)) + "H"
                    adobj.machineState = 2
                    adobj.Remark = ''
                    adobj.save()

                    # 对库存数据进行更改
                    adobj.fk_inventory.fk_structure = Structure.objects.get(name=applyObj.applyUnit)  # 当前部门为 申请部门
                    adobj.fk_inventory.stayTime = ''  # 清空时间 我发现该字段一直就没起到作用
                    adobj.fk_inventory.currRecUser = applyObj.applyUser  # 当前入库者 = 申请者
                    adobj.fk_inventory.currRecDate = datetime.now()  # 当前入库时间 = 确认借出时间
                    adobj.fk_inventory.state = 2  # ("1", "入庫"), ("2", "可申請"), ("3", "被申請"), ("4", "出库")
                    adobj.fk_inventory.save()

            res['result'] = True

        else:

            pass

        return HttpResponse(json.dumps(res), content_type='application/json')


# 進入申請單詳情編輯界面
# 思路：1. 点击机台借出确认 > 弹出一个remark输入框，该remark，仍然为申请单的备注(备注中可以写到 全部借出或者部分借出等内容等等) >
#      2. 点击保存后 > 进入post方法，此处就需要将applydetailId传递过来，因为这里是部分确认，勾选的表示借出，不勾选的表示未借出，>
#      3. 勾选的逻辑

# 思路：获取到ApplyID > 循环遍历ApplyDetail >
# > 将applydetail中的 借出時長、機台確認狀態、Remark為''、借出日期 > 【借出时长，用于记录机台记录上一次历史的信息】
# > 接着更新Apply单中的数据（申请时长，申请单状态，申请单备注，） >
# > 最后，申请单信息改完，那么就是 库存表 当前使用部门、当前部门停留时间、当前入库接收者、当前入库接收时间、状态
# > 更改完成之后，一个申请流程结束， 进入机台状况查询。。

#      4. 不勾选的逻辑
# 思路：没有勾选的 applydetail >  借出时长（直接一杆，表示未借出）、机台确认状态（拒绝）、Remark(可以修改为自定义)、借出日期（保留，为拒绝日期）、
# 借出单位（拒绝单位）、机台申请前状态(可以赋值上去)、确认人（拒绝人）
# apply中 > lendRemark变化 申请时长、申请单状态
# 库存表、 当前使用部门(不变)，当前部门停留时间(不变)、当前入库接收者(不变)、当前入库接收时间(不变)、状态(不变)

class LoanConfirmMachRemarkView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        # 同时确认多个单，需要传递多个单的applyId
        # id_list = map(int, request.POST.get('applyId').split(','))
        ret['applyId'] = request.GET.get('applyId')
        ret['applyDetailIds'] = request.GET.get('applyDetailIds')
        return render(request, 'dqe/LoanConfirm/ApplyRemark.html', ret)

    # 一次確認一個單或一次確認多個單
    def post(self, request):
        res = dict(result=False)
        print('56454545', request.POST)
        # 进入此处可获取 applyId / applyDetailIds
        if 'arrlyId' in request.POST and request.POST['arrlyId']:
            # 获取该申请单的id
            applyObj = Apply.objects.get(id=request.POST.get('arrlyId'))
            print('//////', applyObj)
            # 更新Apply表中的数据
            at = datetime.now() - applyObj.applyDate
            applyObj.applyTime = str(at.days) + "D" + " " + str(
                floor(at.seconds / 60 / 60)) + "H"  # 申请时长 = 确认日期（当前确认的时间） - 申请日期
            applyObj.applyState = 2  # ("1", "待簽核"), ("2", "已簽核"),
            applyObj.lendRemark = request.POST.get("lendRemark")
            applyObj.save()

            # 查找该单下所有的applydetail对象
            adobjs = ApplyDetail.objects.filter(fk_apply=applyObj)  # 状态：("1", "未確認"), ("2", "確認"), ("3", "拒絕"),
            adids = [adobj.id for adobj in adobjs]  # 申请单下的所有applydetailid

            # --0227Add Forest--
            # 增加if语句用于判断拒绝签核 ，如果没有勾选，则表示全部拒绝
            if request.POST.get('arrlyDetailIds'):
                adid_list = list(map(int, request.POST.get('arrlyDetailIds').split(',')))  # 借出勾选的applyDetailId
            else:
                adid_list = []
            adid_differ = list(set(adids) - set(adid_list))  # 未借出的applyDetailId

            # 遍历整个ApplyDetail
            for adobj in adobjs:
                # 勾选
                if adobj.id in adid_list:
                    adobj.lendDate = datetime.now()
                    lt = datetime.now()
                    # 字符串时间格式转化
                    if adobj.lendUnit == "PM":  # 确认单位为PM时，对PM单位停留时间的统计需要特殊的处理
                        # if adobj.fk_inventory.currRecDate == " ":  #初次入库的时候，机台当前入库时间是为空的，应该以入库时间为准
                        #     lt = adobj.lendDate - datetime.strptime(adobj.fk_inventory.indate, '%Y-%m-%d %H:%M:%S.%f')  # 借出时长 = 借出日期 - 入库时间  历史
                        # else:
                        # 当机台第二次从PM借出去时，当前入库时间不为空
                        lt = adobj.lendDate - datetime.strptime(adobj.fk_inventory.currRecDate,
                                                                '%Y-%m-%d %H:%M:%S.%f')  # 借出时长 = 借出日期 - 机台当前入库时间  历史
                    else:
                        lt = adobj.lendDate - datetime.strptime(adobj.fk_inventory.currRecDate,
                                                                '%Y-%m-%d %H:%M:%S.%f')  # 借出时长 = 借出日期 - 机台当前入库时间  历史

                    adobj.lendtime = str(lt.days) + "D" + " " + str(floor(lt.seconds / 60 / 60)) + "H"
                    adobj.machineState = 2
                    adobj.Remark = ''
                    adobj.save()

                    # 对库存数据进行更改之前应该先保存在该部门下的停留时间（后面统计在各个部门下的停留时间2019.2.12carl）
                    # 先查询该部门是否以前借过，若没有，则新建；若已经借过，时间累加
                    list_obj_recordTable = RecordTable.objects.filter(fk_inventory=adobj.fk_inventory)
                    # print("++++++++++++++++++++++")
                    # print(list_obj_recordTable)
                    if list_obj_recordTable:
                        for i_obj_record in list_obj_recordTable:
                            # 存在该部门的记录，则以前借过该机台，时间应该进行累加
                            if i_obj_record.fk_structure == adobj.fk_inventory.fk_structure:
                                list_D_H = re.findall(r'\d+',
                                                      i_obj_record.stayTimeTotal)  # 第一个数字为D，第二个数字为H  ﻿['1', '22']
                                new_record_time = str(int(lt.days) + int(list_D_H[0])) + "D" + " " + str(
                                    int(floor(lt.seconds / 60 / 60)) + int(list_D_H[1])) + "H"
                                i_obj_record.stayTimeTotal = new_record_time
                                i_obj_record.save()
                            # 不存在该部门记录，新建
                            else:
                                RecordTable.objects.create(fk_inventory=adobj.fk_inventory,
                                                           fk_structure=adobj.fk_inventory.fk_structure,
                                                           stayTimeTotal=adobj.lendtime)
                    else:
                        # 查询不到任何记录也新建

                        RecordTable.objects.create(fk_inventory=adobj.fk_inventory,
                                                   fk_structure=adobj.fk_inventory.fk_structure,
                                                   stayTimeTotal=adobj.lendtime)
                    # print("+++++++++++++++++++++++++")

                    # 对库存数据进行更改
                    adobj.fk_inventory.fk_structure = Structure.objects.get(name=applyObj.applyUnit)  # 当前部门为 申请部门
                    adobj.fk_inventory.stayTime = ''  # 清空时间 我发现该字段一直就没起到作用
                    adobj.fk_inventory.currRecUser = applyObj.applyUser  # 当前入库者 = 申请者
                    adobj.fk_inventory.currRecDate = datetime.now()  # 当前入库时间 = 确认借出时间
                    adobj.fk_inventory.state = 2  # ("1", "入庫"), ("2", "可申請"), ("3", "被申請"), ("4", "出库")
                    adobj.fk_inventory.save()
                    adobj.save()

                # 未勾选
                elif adobj.id in adid_differ:
                    adobj.machineState = 3  # 設為拒絕狀態
                    adobj.confirmUser = request.user.name  # 拒收人姓名
                    adobj.lendDate = datetime.now()  # 拒收日期
                    # adobj.lendUnit = request.user.department #拒絕單位
                    adobj.lendtime = "沒借出"  # 没借出、這裡也可以显示为空
                    adobj.Remark = '沒借出'  # 默認就設為空
                    # -- 2019-3-2判断，如果 当前入库日期 不等于 入库日期，那么状态则为 可申请，反之则为 入库。为什么这么改，因为申请一个单的时候，状态会变为被申请(否决)
                    #                     if datetime.strptime(adobj.fk_inventory.currRecDate,'%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d') != adobj.fk_inventory.indate.strftime('%Y-%m-%d'):
                    #                         adobj.macAppState = 2   #adobj.fk_inventory.state   #机台申请前状态
                    #                     else:
                    #                         adobj.macAppState = 1
                    # adobj.macAppState = adobj.fk_inventory.state 注释掉，之前申请时已经有了

                    adobj.fk_inventory.state = 1  # ("1", "入庫"), ("2", "可申請"), ("3", "被申請"), ("4", "出库")
                    adobj.fk_inventory.save()
                    adobj.save()

                    # 对库存数据进行更改 （库存就不需要更改）
                else:
                    pass

            res['result'] = True

        else:
            res['result'] = False

        return HttpResponse(json.dumps(res), content_type='application/json')


# 新增备注
class LoanConfirmAddRemarkView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        # 根据applyDetailId ，修改该对象中的remark
        # id_list = list(map(int, request.POST.get('applyId').split(',')))

        ret['applyDetailId'] = request.GET.get('applyDetailId')

        return render(request, 'dqe/LoanConfirm/ApplyDetailRemark.html', ret)

    def post(self, request):
        res = dict(result=False)

        adObj = ApplyDetail.objects.get(id=request.POST.get('applyDetailId'))
        adObj.remark = request.POST.get('remark')
        adObj.save()

        res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


# message铃铛
class LoanConfirmMessageView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict()

        # res = dict(data=list(Apply.objects.filter(applyState=1).values('applyState').annotate(count=Count('applyState').values('applyState','count')))) #.order_by('-属性')

        # 统计applyState为待签核的状态的数据
        # res['data'] = list(Apply.objects.filter(applyState=1,applydetail__lendUnit=request.user.department).values('id','applyState','applydetail__lendUnit').distinct().annotate(count=Count('applyState')).values('applyState','count'))

        count = Apply.objects.filter(applyState=1, applydetail__lendUnit=request.user.department).values('id',
                                                                                                         'applyState',
                                                                                                         'applydetail__lendUnit').distinct().count()

        res['data'] = [{'applyState': '1', 'count': count}]

        # 如果沒有待簽核的,把0传递过去
        if res['data'] == []:
            res['data'] = [{'applyState': '1', 'count': 0}]

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
