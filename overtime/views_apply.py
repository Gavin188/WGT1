import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views import View

from dqe.models import ApplyListDetail
from overtime.models import ApplyList, Abnormal, Absent, AddTime, AddMonth
from system.mixin import LoginRequiredMixin
from system.models import Menu, Structure


# 申请单明细
class ApplyListView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=ApplyList.objects.all())
        menu = Menu.get_menu_by_request_url(url=self.request.path_info)

        applyState_list = []

        for applyState in ApplyList.APPLYSTATE_TYPE:
            applyState_dict = dict(key=applyState[0], value=applyState[1])
            applyState_list.append(applyState_dict)

        res['applyState_list'] = applyState_list

        if menu is not None:
            res.update(menu)
        return render(request, 'overtime/apply/Apply_List.html', res)


# 显示申请单信息
class ApplyDetailView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'applyNum', 'applyType', 'applyUser', 'applyDate', 'applyUnit', 'applyState',
                  'confirmUser', 'confirmTime']
        # 搜索框
        searchFields = ['applyDate', 'applyState']

        #  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   i not in ['', ] and request.GET.get(i, '')}

        filters['applyUser'] = request.user.username
        res = dict(data=list(ApplyList.objects.filter(**filters).values(*fields).order_by('-applyDate')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 删除申请单
class ApplyDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        # todo: 获取后台传来的多个ID ，
        if 'id' in request.POST and request.POST['id']:
            # todo: 装换成int
            id_list = list(map(int, request.POST.get('id').split(',')))
            month_id = list(ApplyList.objects.filter(id__in=id_list).values('fk_month_id'))
            # 删除外键
            month_list = [i['fk_month_id'] for i in month_id]
            if month_id:
                AddMonth.objects.filter(id__in=month_list).delete()
            ApplyList.objects.filter(id__in=id_list).delete()
            res['result'] = True

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type="application/json")


class ApplyAbnormalView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            apply = get_object_or_404(ApplyList, pk=request.GET.get('id'))
        ret['apply'] = apply
        return render(request, 'overtime/apply/Abnormal_detail.html', ret)


# 显示请假申请详情列表
class ApplyAbnormalistView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'username__name', 'username__username', 'username__level', 'username__mobile', 'leave_type',
                  'startTime',
                  'lengh_time',
                  'time_start_period', 'endTime', 'time_end_period', 'reason', 'agent_name',
                  'agent_worknum',
                  'fk_apply__applyState', 'fk_apply__confirmUser']
        filter = {}

        filter['fk_apply_id'] = request.GET.get('applyId')

        res = dict(data=list(Abnormal.objects.filter(**filter).values(*fields).order_by('-apply_time')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class ApplyAbsentView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            apply = get_object_or_404(ApplyList, pk=request.GET.get('id'))
        ret['apply'] = apply

        return render(request, 'overtime/apply/Absent_detail.html', ret)


class ApplyAbsentlistView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'username__name', 'username__username', 'username__level', 'username__mobile', 'absent_type',
                  'startTime', 'card_type', 'time_end_period', 'reason', 'fk_apply__applyState',
                  'fk_apply__confirmUser']
        filter = {}

        filter['fk_apply_id'] = request.GET.get('applyId')

        res = dict(data=list(Absent.objects.filter(**filter).values(*fields).order_by('-apply_time')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 请假和异常加班提示信息   message铃铛
'''
1, 先获取 数据库中 数量、 状态、 确认单位 
2， js 每隔一秒 刷新获取到 值
3， 将获取的值显示出来

'''


class OvertimeMessageView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict()

        # res = dict(data=list(Apply.objects.filter(applyState=1).values('applyState').annotate(count=Count('applyState').values('applyState','count')))) #.order_by('-属性')

        # 统计applyState为待签核的状态的数据
        # res['data'] = list(Apply.objects.filter(applyState=1,applydetail__lendUnit=request.user.department).values('id','applyState','applydetail__lendUnit').distinct().annotate(count=Count('applyState')).values('applyState','count'))

        count = ApplyList.objects.filter(applyState=1).values('id', 'applyState').distinct().count()

        # count1 = ApplyList.objects.filter(applyState=1, accessorylistdetail__lendUnit=request.user.department).values(
        #     'id',
        #     'applyState',
        #     'accessorylistdetail__lendUnit').distinct().count()

        # count = count + count1
        # print('count--->', count)

        res['data'] = [{'applyState': '1', 'count': count, 'confirmUnit': 'Leader'}]

        # 如果沒有待簽核的,把0传递过去
        if res['data'] == []:
            res['data'] = [{'applyState': '1', 'count': 0}]

        # print(res['data'])

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class ApplyLeaderListView(LoginRequiredMixin, View):
    def get(self, request):
        # res = dict(data=ApplyList.objects.all())
        # time = datetime.date.today()
        # res['time'] = time
        # print(res)
        # menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        # if menu is not None:
        #     res.update(menu)

        res = dict(data=ApplyList.objects.all())

        # 機台確認狀態
        machineState_list = []
        for machineState in ApplyList.APPLYSTATE_TYPE:
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

        return render(request, 'overtime/apply/ApplyLeader_List.html', res)


class ApplyLeaderDetailView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'applyNum', 'applyType', 'applyUser', 'applyDate', 'applyUnit', 'applyState',
                  'confirmUser', 'confirmTime']
        searchFields = ['applyDate', 'applyUnit', 'applyUser', 'applyState']  # 与数据库字段一致
        # print(request.GET)
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   i not in ['', ] and request.GET.get(i,
                                                       '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
        # print('**', filters)
        # filter['applyUser'] = request.user.username
        res = dict(data=list(ApplyList.objects.filter(**filters).values(*fields).order_by('-applyDate')))

        # print('res--', res)

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 删除申请单
class ApplyLeaderDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        id = request.POST.get('id')

        ApplyList.objects.get(id=id).delete()
        res['result'] = True

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type="application/json")


class ApplyLeaderAbnormalView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            apply = get_object_or_404(ApplyList, pk=request.GET.get('id'))
        ret['apply'] = apply

        return render(request, 'overtime/apply/AbnormalLeader_detail.html', ret)


# 显示请假申请详情列表
class ApplyLeaderAbnormalistView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'username__name', 'username__username', 'username__level', 'username__mobile', 'leave_type',
                  'startTime',
                  'lengh_time',
                  'time_start_period', 'endTime', 'time_end_period', 'reason', 'agent_name',
                  'agent_worknum',
                  'fk_apply__applyState', 'fk_apply__confirmUser']
        filter = {}

        filter['fk_apply_id'] = request.GET.get('applyId')

        res = dict(data=list(Abnormal.objects.filter(**filter).values(*fields).order_by('-apply_time')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class ApplyLeaderAbsentView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            apply = get_object_or_404(ApplyList, pk=request.GET.get('id'))
        ret['apply'] = apply

        return render(request, 'overtime/apply/AbsentLeader_detail.html', ret)


class ApplyLeaderAbsentlistView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'username__name', 'username__username', 'username__level', 'username__mobile', 'absent_type',
                  'startTime', 'card_type', 'time_end_period', 'reason', 'fk_apply__applyState',
                  'fk_apply__confirmUser']
        filter = {}

        filter['fk_apply_id'] = request.GET.get('applyId')

        res = dict(data=list(Absent.objects.filter(**filter).values(*fields).order_by('-apply_time')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# --------确认申请单-------------------------------
# 同意请假
class ApplyConfirmView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        applyId = request.POST.get('id')
        # print(applyId)
        data = ApplyList.objects.get(id=applyId)
        data.applyState = 2
        data.confirmTime = datetime.datetime.now()
        data.confirmUser = request.user.name
        data.save()
        res['result'] = True
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 拒绝请假
class ApplyRefuseView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        applyId = request.POST.get('id')
        # print(applyId)
        data = ApplyList.objects.get(id=applyId)
        data.applyState = 4
        data.confirmTime = datetime.datetime.now()
        data.confirmUser = request.user.name
        data.save()
        res['result'] = True
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


#  加班详情
class ApplyAddTimeView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            apply = get_object_or_404(ApplyList, pk=request.GET.get('id'))
        ret['apply'] = apply

        return render(request, 'overtime/apply/AddTime_detail.html', ret)


# 加班详情列表
class ApplyAddTimelistView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'username__name', 'username__username', 'username__level', 'data_time', 'data_hour',
                  'data_type', 'add_content', 'fk_apply__applyState',
                  'fk_apply__confirmUser']
        filter = {}

        filter['fk_apply_id'] = request.GET.get('applyId')

        res = dict(data=list(AddTime.objects.filter(**filter).values(*fields).order_by('-data_type')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 主管 加班详情
class ApplyLeaderAddTimeView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            apply = get_object_or_404(ApplyList, pk=request.GET.get('id'))
        ret['apply'] = apply
        return render(request, 'overtime/apply/AddTimeLeader_detail.html', ret)


# 主管 加班详情列表
class ApplyLeaderAddTimelistView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'username__name', 'username__username', 'username__level', 'data_time', 'data_hour',
                  'data_type', 'add_content', 'fk_apply__applyState',
                  'fk_apply__confirmUser']
        filter = {}

        filter['fk_apply_id'] = request.GET.get('applyId')

        res = dict(data=list(AddTime.objects.filter(**filter).values(*fields).order_by('-data_type')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
