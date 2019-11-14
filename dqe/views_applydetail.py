import json
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import View

from dqe.models import ApplyListDetail, ApplyList, AccessoryListDetail, Project, Stage, Fused
from system.mixin import LoginRequiredMixin
from system.models import Menu, Structure, Access


class ApplyDetailView(LoginRequiredMixin, View):
    '''借入申请页面'''

    def get(self, request):
        res = dict(data=ApplyListDetail.objects.all())

        # 機台確認狀態
        machineState_list = []
        for machineState in ApplyListDetail.MACHINE_STATE:
            machineState_dict = dict(key=machineState[0], value=machineState[1])
            machineState_list.append(machineState_dict)
        res['machineState_list'] = machineState_list

        # 部門
        structures = Structure.objects.all()
        res['structures'] = structures

        # 申請單狀態
        applyState_list = []
        for applyState in ApplyList.APPLYSTATE_TYPE:
            applyState_dict = dict(key=applyState[0], value=applyState[1])
            applyState_list.append(applyState_dict)
        res['applyState_list'] = applyState_list

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)

        return render(request, 'dqe/ApplyDetail/ApplyDetail_List.html', res)


class ApplyDetailListView(LoginRequiredMixin, View):
    '''申请详情列表'''

    def get(self, request):
        fields = ['id', 'applyNum', 'applyName', 'applyUser', 'applyDate', 'applyUnit', 'applyState', 'lendRemark']

        # 与数据库字段一致
        searchFields = ['applyDate', 'applyUnit', 'applyUser', 'applyState']

        # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   i not in ['', ] and request.GET.get(i, '')}
        # 根据条件 查询的数据
        res = dict(data=list(ApplyList.objects.filter(**filters).values(*fields).order_by('-applyDate')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class ApplyDetailDeleteView(LoginRequiredMixin, View):
    '''申请单删除'''

    def post(self, request):
        res = dict(result=False)

        if 'id' in request.POST and request.POST['id']:
            id_list = list(map(int, request.POST.get('id').split(',')))

            # 根据相应的ID 筛选出申请单的状态，
            aplystate = list(ApplyList.objects.filter(id__in=id_list).values('applyState').distinct())

            # 如果状态是已经签核，则无法删除
            data_list = [i['applyState'] for i in aplystate if i['applyState'] == '2']

            # 判断是否存在。如果存在就提示错误
            if data_list:
                res['result'] = False
                res['message'] = '已经签核的申请单无法删除!'
            else:
                ApplyList.objects.filter(id__in=id_list).delete()
                res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


class ApplyIPadDetailView(LoginRequiredMixin, View):
    '''进入Ipad申請單詳情界面'''

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            applylist = get_object_or_404(ApplyList, pk=request.GET.get('id'))

        ret['applylist'] = applylist

        return render(request, 'dqe/ApplyDetail/ApplyIpad_Detail.html', ret)


class ApplyAccessDetailView(LoginRequiredMixin, View):
    '''进入 配件 申请详情界面'''

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            applylist = get_object_or_404(ApplyList, pk=request.GET.get('id'))

        ret['applylist'] = applylist

        return render(request, 'dqe/ApplyDetail/ApplyAccess_Detail.html', ret)


class ApplyIpadListView(LoginRequiredMixin, View):
    '''Ipad申请详情列表'''

    def get(self, request):
        fields = ['id', 'sn', 'machineState', 'lendUnit', 'qty',
                  'comments', 'model', 'timeState', 'platform',
                  'stage', 'type', 'fk_apply__applyUser', 'fk_apply__applyUnit',
                  'applyDate', 'fk_apply__lendRemark', 'lendDate']

        # 搜索框 ，根据条件查询数据
        searchFields = ['platform', 'machineState', ]
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        # 通过隐含传递的applyId，反向查出applydetail中所有对应该applyId的信息
        filters['fk_apply_id'] = request.GET.get('applyId')

        #  # 查询ApplyDetail所有结果
        res = dict(
            data=list(ApplyListDetail.objects.filter(**filters).values(*fields).order_by('-fk_apply__applyDate')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class AccesssoryView(LoginRequiredMixin, View):
    '''配件申请详情列表'''

    def get(self, request):
        fields = ['id', 'machineState', 'lendUnit', 'qty',
                  'comments', 'accessory', 'timeState',
                  'stage', 'fk_apply__applyUser', 'fk_apply__applyUnit',
                  'applyDate', 'fk_apply__lendRemark', 'lendDate']

        # 搜索框 ，根据条件查询数据
        searchFields = ['platform', 'machineState', ]
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        # 通过隐含传递的applyId，反向查出applydetail中所有对应该applyId的信息
        filters['fk_apply_id'] = request.GET.get('applyId')
        # 根据条件查询数据
        res = dict(
            data=list(AccessoryListDetail.objects.filter(**filters).values(*fields).order_by('-fk_apply__applyDate')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class ApplyDetailUpdateView(LoginRequiredMixin, View):
    ''' 修改IPad 申请单'''

    def get(self, request):
        # 申请详情单id
        id = request.GET.get('id')

        # 申请单id
        apply_id = request.GET.get('apply_id')

        # 获取修改前的值
        apply_list = list(ApplyListDetail.objects.filter(id=id).values())[0]

        # 平台
        projects = Project.objects.all()

        # 階段
        stages = Stage.objects.all()

        # 版本
        fuseds = Fused.objects.all()

        # 机台版本狀態 wifi or 3g
        applyState_list = []
        for applyState in Fused.STATE_TYPE:
            applyState_dict = dict(key=applyState[0], value=applyState[1])
            applyState_list.append(applyState_dict)

        #  一天还是长借
        timeState_list = []
        for timeState in Fused.TIME_TYPE:
            timeState_dict = dict(key=timeState[0], value=timeState[1])
            timeState_list.append(timeState_dict)

        context = {
            'apply_id': apply_id,
            'id': id,
            'projects': projects,
            'stages': stages,
            'fuseds': fuseds,
            'applyState_list': applyState_list,
            'timeState_list': timeState_list,
            'apply_list': apply_list,
        }

        return render(request, 'dqe/ApplyDetail/ApplyDetail_Update.html', context)

    def post(self, request):
        # 获取修改的表单内容和
        res = dict(result=False)
        id = request.POST.get('id')
        platform = request.POST.get('platform')
        stage = request.POST.get('stage')
        model = request.POST.get('model')
        type = request.POST.get('type')
        comments = request.POST.get('comments')
        timeState = request.POST.get('timeState')
        qty = request.POST.get('qty')
        # apply_id = request.POST.get('apply_id')

        # 将数据保存到数据库中
        try:
            apply_detail = ApplyListDetail.objects.get(id=id)
            apply_detail.platform = platform
            apply_detail.stage = stage
            apply_detail.model = model
            apply_detail.type = type
            apply_detail.qty = qty
            apply_detail.comments = comments
            apply_detail.timeState = timeState
            apply_detail.applyDate = datetime.now()

            apply_detail.save()
            res['result'] = True
        except ApplyList.DoesNotExist:
            # 申请单不存在
            res['result'] = False

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class ApplyDetailDelIdView(LoginRequiredMixin, View):
    '''删除申请详情单'''

    def post(self, request):
        res = dict(result=False)

        if 'id' in request.POST and request.POST['id']:
            id = request.POST.get('id')
            apply_id = request.POST.get('apply_id')
            # 根据相应的ID 筛选出申请单的状态，

            applystate = list(ApplyListDetail.objects.filter(id=id).values('machineState'))
            # 如果状态是已经签核，则无法删除

            data_list = [i['machineState'] for i in applystate if i['machineState'] == '2']

            # 判断是否存在。如果存在就提示错误
            if data_list:
                res['result'] = False
                res['message'] = '已经确认的申请单无法删除!'
            else:
                ApplyListDetail.objects.filter(id=id).delete()
                res['result'] = 2

            # 判断 申请单中是否还有申请详情单，如果有则不变，没有数据将申请单删除
            count = ApplyListDetail.objects.filter(fk_apply__id=apply_id).count()
            if count == 0:
                ApplyList.objects.filter(id=apply_id).delete()
                res['result'] = 1

        return HttpResponse(json.dumps(res), content_type='application/json')


class BorrowAccessUpdateView(LoginRequiredMixin, View):
    '''修改 配件 申请详情单'''

    def get(self, request):
        # 申请详情单id
        id = request.GET.get('id')

        # 申请单id
        apply_id = request.GET.get('apply_id')

        # 获取修改前的值
        apply_list = list(AccessoryListDetail.objects.filter(id=id).values())[0]

        # 階段
        stages = Stage.objects.all()

        # 配件
        access = Access.objects.all()

        #  一天还是长借
        timeState_list = []
        for timeState in Fused.TIME_TYPE:
            timeState_dict = dict(key=timeState[0], value=timeState[1])
            timeState_list.append(timeState_dict)

        context = {
            'apply_id': apply_id,
            'id': id,
            'stages': stages,
            'access': access,
            'timeState_list': timeState_list,
            'apply_list': apply_list,
        }

        return render(request, 'dqe/ApplyDetail/Access_Update.html', context)

    def post(self, request):
        # 获取修改的表单内容和
        res = dict(result=False)
        id = request.POST.get('id')
        platform = request.POST.get('platform')
        stage = request.POST.get('stage')
        comments = request.POST.get('comments')
        timeState = request.POST.get('timeState')
        qty = request.POST.get('qty')

        # 将数据保存到数据库中
        try:
            apply_detail = AccessoryListDetail.objects.get(id=id)
            apply_detail.accessory = platform
            apply_detail.stage = stage
            apply_detail.qty = qty
            apply_detail.comments = comments
            apply_detail.timeState = timeState
            apply_detail.applyDate = datetime.now()

            apply_detail.save()
            res['result'] = True
        except ApplyList.DoesNotExist:
            # 申请单不存在
            res['result'] = False

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class BorrowAccessDelView(LoginRequiredMixin, View):
    '''删除配件申请单详情'''

    def post(self, request):
        res = dict(result=False)

        if 'id' in request.POST and request.POST['id']:
            id = request.POST.get('id')

            apply_id = request.POST.get('apply_id')
            # 根据相应的ID 筛选出申请单的状态，

            applystate = list(AccessoryListDetail.objects.filter(id=id).values('machineState'))
            # 如果状态是已经签核，则无法删除

            data_list = [i['machineState'] for i in applystate if i['machineState'] == '2']

            # 判断是否存在。如果存在就提示错误
            if data_list:
                res['result'] = False
                res['message'] = '已经确认的申请单无法删除!'
            else:
                AccessoryListDetail.objects.filter(id=id).delete()
                res['result'] = 2

            # 判断 申请单中是否还有申请详情单，如果有则不变，没有数据将申请单删除
            count = AccessoryListDetail.objects.filter(fk_apply__id=apply_id).count()
            if count == 0:
                ApplyList.objects.filter(id=apply_id).delete()
                res['result'] = 1
        return HttpResponse(json.dumps(res), content_type='application/json')
