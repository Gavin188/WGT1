# Create your views here.
import datetime
import json
import re

from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from overtime.abnormal_report import abnormal_report
from overtime.absent_report import absent_report
from overtime.addtime_report import addTime_report
from overtime.models import TimeType, ApplyList, AddTime, AddMonth, Abnormal, Absent
from overtime.time_transformation import time_tran
from system.mixin import LoginRequiredMixin
# 加班申请
from system.models import UserProfile

'''
1 根据用户提交的加班信息 选取出加班时间
2 再 从数据库中 查找本月的加班情况，将每一天的加班时间进行统计，如果超过30% 则拒绝加班

'''


class TimeListView(LoginRequiredMixin, View):
    def get(self, request):
        name = request.user.username
        time_control = list(UserProfile.objects.filter(username=name).values('time_control'))[0]['time_control']
        res = dict(data=TimeType.objects.filter(time_control=time_control).all())
        # apply_id = list(
        #     AddTime.objects.filter(fk_apply__fk_month__month=datetime.date.today().strftime('%Y-%m'),
        #                            fk_apply__applyState=2,
        #                            username__username=request.user.username).values(
        #         'fk_apply_id'))[0]['fk_apply_id']
        # print('ID --- ', apply_id)
        # res['apply_id'] = apply_id
        return render(request, 'overtime/AddTime/addTime.html', res)

    #  {'2019-8-3': ['10'], '2019-8-10': ['10'], '2019-8-24': ['10'], '2019-8-5': ['2'], '2019-8-12': ['2'], '2019-8-19': ['2'], 'tic': ['36']}
    def post(self, request):

        # 获取当前用户的 加班管控
        name = request.user.username
        time_control = list(UserProfile.objects.filter(username=name).values('time_control'))[0]['time_control']

        day_Exceed = []
        res = dict(result=False)
        data = dict(request.POST)
        id = request.POST.get('user_id')
        user = UserProfile.objects.get(id=id)

        # 获取所有人的个数
        user_count = UserProfile.objects.count()

        #  根据提报的当天日期，求出下个月的时间
        today = datetime.date.today()
        date = today.strftime('%d')  # 当前年份月份
        ne_today = today - relativedelta(months=-1)
        next_today = ne_today.strftime('%Y-%m')
        year_month = data['YM'][0]
        print('year ---', year_month)
        #  管理员管控的加班权限 ，加班比例
        scale = list(TimeType.objects.filter(time_control=time_control).values('tscale'))[0]['tscale']
        #  管理员管控的加班权限 ，加班提报日期
        tdate = list(TimeType.objects.filter(time_control=time_control).values('tdate'))[0]['tdate']
        fesday = data['fesDay[]']
        del data['user_id']
        del data['tic']
        del data['YM']
        # del data['apply_id']
        print('-->', data)
        del data['fesDay[]']
        # 获取后台时间判断是否提报的下一个月的加班，
        # 并且将后台传来的时间转换成相应的格式 2019-8 ->  2019-08
        if len(year_month) == 6:
            year_month = list(year_month)
            year_month.insert(5, '0')
            year_month = ''.join(year_month)
        if date == tdate:
            if year_month == next_today:  # 2019-10

                state = list(ApplyList.objects.filter(applyUser=request.user.username,
                                                      fk_month__month=year_month).values(
                    'applyState').distinct())
                state = [i['applyState'] for i in state]
                if '2' not in state:
                    # 获取下个月的时间
                    today = datetime.date.today() - relativedelta(months=-1)
                    add_month = AddMonth()
                    add_month.month = str(today)[0:7]
                    add_month.save()
                    # print(today)
                    for day in data.keys():
                        # 排除周六
                        if int(data[day][0]) < 8:
                            '''
                             获取到某个人 某个月平时的加班时间
                             从数据库查询 某一天的人数
                             用 人数 / 总数 = 概率 
                            '''
                            data_count = AddTime.objects.filter(fk_apply__fk_month__month=next_today,
                                                                fk_apply__applyState=2,
                                                                data_time=day).count()
                            percentage = (data_count + 1) / user_count  # 总数
                            # print('percentage', str(percentage)[:3])
                            if str(percentage)[:4] < scale:
                                pass
                            else:
                                day_Exceed.append(day)
                    # print(day_Exceed)
                    if len(day_Exceed) == 0:
                        # print(1111)
                        apply_num = str(request.user.name) + "-" + '加班' + "-" + str(
                            datetime.datetime.now().strftime('%Y%m%d_%H%M'))
                        applyList = ApplyList()
                        applyList.applyUser = request.user.username
                        applyList.applyUnit = request.user.department  # 申請單位
                        applyList.applyDate = datetime.datetime.now()
                        applyList.applyNum = apply_num
                        applyList.applyState = 1  # ("1", "待簽核"), ("2", "已簽核"),("3","已取消")
                        applyList.applyType = 3  # ('1', '请假'),('2','异常'),("3","加班")
                        applyList.fk_month = add_month
                        applyList.save()

                        for k, v in data.items():
                            if int(v[0]) == 2:
                                add_time = AddTime()
                                add_time.fk_apply = applyList
                                add_time.username = user
                                add_time.add_content = "白手套实验"
                                # add_time.save(commit=False)
                                add_time.data_time = time_tran(k)
                                add_time.data_hour = int(v[0])
                                add_time.data_type = 'G1'
                                add_time.save()

                            elif 2 < int(v[0]) <= 10:
                                if k in fesday:
                                    add_time = AddTime()
                                    add_time.fk_apply = applyList
                                    add_time.username = user
                                    add_time.add_content = "白手套实验"
                                    # add_time.save(commit=False)
                                    add_time.data_time = time_tran(k)
                                    add_time.data_hour = int(v[0])
                                    add_time.data_type = 'G3'
                                    # print(k, v)
                                    add_time.save()

                                else:
                                    add_time = AddTime()
                                    add_time.fk_apply = applyList
                                    add_time.username = user
                                    add_time.add_content = "白手套实验"
                                    # add_time.save(commit=False)
                                    add_time.data_time = time_tran(k)
                                    add_time.data_hour = int(v[0])
                                    add_time.data_type = 'G2'
                                    add_time.save()

                        res['result'] = 1
                    else:
                        res['result'] = 2
                        res['day_Exceed'] = day_Exceed
                else:
                    res['result'] = 7
                    res['message'] = year_month + '加班已经确认，请下个月修改'

            elif year_month == today.strftime("%Y-%m"):
                '''
                1、 获取今天的日期  today
                2、 获取今天-以前的加班以及加班总时间
                3、 获取当前用户是否管控， 管控- 以前时间 = 剩余时间
                4、 不能提报 今天以前的加班 只能提报本月和下个月的加班
                5、 将本月的加班 今天以后的加班删除
                6、 获取 今天以前的加班 ， +  今天重新提交的
                # 7 、获取原先的 申请单， 将超过今天的加班删除，添加新的加班
                # 8、 將申請單 狀態 改成 未签核，申请单状态详情 未确认
                #     申请时间变成当成 现在时间
                #     确认时间 删除
                
                7、新建一个申请单，申请详情
                
                '''
                #  获取今天的日期  # 2019-09-11
                time = datetime.date.today()
                #  获取本月份的加班  # 2019-09-11 -> 2019-09
                today = time.strftime('%Y-%m')
                #  获取 本人 这个月的加班状态 （("1", "待簽核"), ("2", "已簽核"), ("3", "已取消"), ("4", "已拒绝"))
                state = list(
                    ApplyList.objects.filter(applyUser=request.user.username, fk_month__month=today).values(
                        'applyState').distinct())
                state = [i['applyState'] for i in state]
                print('state--', state)
                if '1' not in state:

                    #  时间：本月的时间， 状态：已经签核， 用户： 本人，
                    #  本月的加班详情 #
                    #  [{'data_time': '2019-09-21', 'data_hour': '10'}, {'data_time': '2019-09-14', 'data_hour': '10'},
                    #  {'data_time': '2019-09-07', 'data_hour': '10'},{'data_time': '2019-09-02', 'data_hour': '2'},
                    #  {'data_time': '2019-09-09', 'data_hour': '2'}, {'data_time': '2019-09-16', 'data_hour': '2'}]
                    month = list(AddTime.objects.filter(fk_apply__fk_month__month=today, fk_apply__applyState=2,
                                                        username__username=request.user.username).values(
                        'data_time',
                        'data_hour',
                        'data_type'))

                    before_list = []
                    time_list = []
                    for i in month:
                        #  判断 如果 提报时间 小于 今天的日期， 放到 before_list
                        if i['data_time'] < str(time):
                            date_dict = {}
                            date_dict[i['data_time']] = i['data_hour']
                            before_list.append(date_dict)
                        #  将上个月提报的本月加班，所有的时间和小时 以字典的形式显示 - - >  为了求出今天以前的加班时数，和缺少的加班时数
                        time_dict = {}
                        time_dict[i['data_time']] = i['data_hour']
                        time_list.append(time_dict)
                    #  通过加班管控，求出本人这个月加班的总时数，
                    control_time = list(TimeType.objects.filter(time_control=time_control).values('tname'))[0][
                        'tname']

                    # print(control_time)
                    before_tiem = 0
                    # 判断 今天以前的加班时数  before_tiem
                    for i in before_list:
                        for k, v in i.items():
                            before_tiem = before_tiem + int(v)  # 已加班时数

                    #  本月加班的总时数 -  已经加班时数
                    after_time = int(control_time) - before_tiem  # 为加班时数

                    count = 0
                    flag = False
                    #  循环 提报的本月的加班时数 求出 系统修改 提报的时数  count
                    for k, v in data.items():
                        if time_tran(k) < str(time):
                            flag = False
                            res['result'] = 3
                            res['message'] = '不能提报超过' + str(time) + '的日期'
                            break
                        else:
                            flag = True
                            count = count + int(v[0])
                    # print('count--', count)
                    if flag:
                        # 如果提报的时数大于 未加班时数
                        if count > after_time:
                            time_poor = count - after_time
                            res['result'] = 5
                            res['message'] = '你应该提报' + str(after_time) + '小时，超了' + str(time_poor) + '小时'
                        else:
                            for day in data.keys():
                                # 排除周六
                                if int(data[day][0]) < 8:
                                    '''
                                     获取到某个人 某个月平时的加班时间
                                     从数据库查询 某一天的人数
                                     用 人数 / 总数 = 概率 
                                    '''
                                    data_count = AddTime.objects.filter(fk_apply__fk_month__month=today,
                                                                        fk_apply__applyState=2,
                                                                        data_time=time_tran(day)).count()

                                    percentage = data_count / user_count  # 总数

                                    if str(percentage)[:4] < scale:
                                        pass
                                    else:
                                        #  超出加班管控比例的天数
                                        day_Exceed.append(day)
                            #  如果没有超过加班管控的天数 ；
                            if len(day_Exceed) == 0:
                                #  求出 上个月提报的 申请单 ID
                                apply_id = list(
                                    AddTime.objects.filter(fk_apply__fk_month__month=today, fk_apply__applyState=2,
                                                           username__username=request.user.username).values(
                                        'fk_apply_id'))[0]['fk_apply_id']
                                res['apply_id'] = apply_id
                                #  将以前提报的加班改成 已取消  同意的话将 已取消 -> 已修改   拒绝 已取消-> 已签核
                                ApplyList.objects.filter(id=apply_id).update(applyState=3)
                                #  创建 本月的加班
                                add_month = AddMonth()
                                add_month.month = today
                                add_month.save()
                                #  创建新的申请单
                                apply_num = str(request.user.name) + "-" + '加班' + "-" + str(
                                    datetime.datetime.now().strftime('%Y%m%d_%H%M'))
                                applyList = ApplyList()
                                applyList.applyUser = request.user.username
                                applyList.applyUnit = request.user.department  # 申請單位
                                applyList.applyDate = datetime.datetime.now()
                                applyList.applyNum = apply_num
                                applyList.applyState = 1  # ("1", "待簽核"), ("2", "已簽核"),("3","已取消")
                                applyList.applyType = 3  # ('1', '请假'),('2','异常'),("3","加班")
                                applyList.fk_month = add_month
                                applyList.save()

                                # 将修改的后加班 的加班时间转换成 字典 ，存入新的申请单
                                for i in before_list:
                                    for k, v in i.items():
                                        data[k] = [v]

                                for k, v in data.items():
                                    if int(v[0]) == 2:
                                        add_time = AddTime()
                                        add_time.fk_apply = applyList
                                        add_time.username = user
                                        add_time.add_content = "白手套实验"
                                        # add_time.save(commit=False)
                                        add_time.data_time = time_tran(k)
                                        add_time.data_hour = int(v[0])
                                        add_time.data_type = 'G1'
                                        add_time.save()

                                    elif 2 < int(v[0]) <= 10:
                                        if k in fesday:
                                            add_time = AddTime()
                                            add_time.fk_apply = applyList
                                            add_time.username = user
                                            add_time.add_content = "白手套实验"
                                            # add_time.save(commit=False)
                                            add_time.data_time = time_tran(k)
                                            add_time.data_hour = int(v[0])
                                            add_time.data_type = 'G3'
                                            # print(k, v)
                                            add_time.save()

                                        else:
                                            add_time = AddTime()
                                            add_time.fk_apply = applyList
                                            add_time.username = user
                                            add_time.add_content = "白手套实验"
                                            # add_time.save(commit=False)
                                            add_time.data_time = time_tran(k)
                                            add_time.data_hour = int(v[0])
                                            add_time.data_type = 'G2'
                                            add_time.save()

                                res['result'] = 1
                            else:
                                res['result'] = 2
                                res['day_Exceed'] = day_Exceed
                else:
                    res['result'] = 6
                    res['message'] = '你本月提报的加班还未确认，不能再提报'

            else:
                res['result'] = 3

                res['message'] = '只能提报本月和下个月的加班'

        else:
            res['result'] = 4
            res['message'] = '当前时间：' + str(today)

        print(res)
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


#  总览加班
class OverViewDetail(LoginRequiredMixin, View):
    def get(self, request):
        res = dict()
        today = datetime.date.today()  # - relativedelta(months=-1)
        next_date = today.strftime('%Y')
        next_moth = today.strftime('%m')

        # print(next_date)
        # print(next_moth)
        res['next_date'] = next_date
        res['next_moth'] = next_moth
        # print('8858', res)
        return render(request, 'overtime/apply/OverViewTime.html', {'data': res})


# 每个月的加班情况
class OverViewMonthListView(LoginRequiredMixin, View):
    def post(self, request):
        filters = {}
        # 获取 后台 查找 u用户
        person = request.POST.get('person')

        if request.POST.get('person'):
            filters['username__name'] = person
        fields = ['id', 'username__name', 'username__username', 'data_time', 'data_hour', 'data_type',
                  'fk_apply__applyNum', 'fk_apply__applyState', 'fk_apply__id']
        res = {"success": "",
               "totalRows": "",
               "curPage": 1,
               "data": " "}
        ret = []
        # 获取查找的时间
        date = request.POST.get('date')
        moth = request.POST.get('moth')
        next_today = date + '-' + moth + '-01'
        month = time_tran(next_today)[0:7]
        # print('moth', month)
        filters['fk_apply__fk_month__month'] = month

        #  查询出 未签核 和 已签核 加班时间
        datas = list(
            AddTime.objects.filter(Q(fk_apply__applyState=1) | Q(fk_apply__applyState=2), **filters).values(*fields))
        #  先查询出 加班的所有用户 放入 arr_per
        # print(datas)
        arr_per = []
        for i in datas:
            if i['username__username'] not in arr_per:
                arr_per.append(i['username__username'])
            # mat = re.search(r"(-\d{1,2})", i['data_time'])
            # data = mat.group(0)
            # print('data-->', i['data_time'])
        for per in arr_per:
            data_ibj = {}
            count = 0
            count1 = 0
            count2 = 0
            for i in datas:
                if i['username__username'] == per:

                    if i['data_type'] == 'G1':
                        count = count + int(i['data_hour'])
                    if i['data_type'] == 'G2':
                        count1 = count1 + int(i['data_hour'])
                    if i['data_type'] == 'G3':
                        count2 = count2 + int(i['data_hour'])

                    Count = count + count1 + count2

                    data_ibj['user_name'] = i['username__name']
                    data_ibj['user_worknum'] = per
                    data_ibj['id'] = i['fk_apply__id']
                    # data_ibj['id'] = list(ApplyList.objects.filter(applyNum=i['fk_apply__applyNum']).values('id'))[0][
                    #     'id']
                    if i['fk_apply__applyState'] == '1':
                        type = '未签核'
                    elif i['fk_apply__applyState'] == '2':
                        type = '已签核'
                    data_ibj['type'] = type
                    data_ibj['G1'] = count
                    data_ibj['G2'] = count1
                    data_ibj['G3'] = count2
                    data_ibj['Count'] = Count
                    data_ibj[time_tran(i['data_time'])[8:]] = i['data_hour']

            ret.append(data_ibj)
            count_sum = len(ret)
            res["totalRows"] = count_sum

        pageIndex = request.POST.get('curPage')
        pageSize = request.POST.get('pageSize')
        pageInator = Paginator(ret, pageSize)
        contacts = pageInator.page(pageIndex)
        data_list = []  # 最终返回的结果集合
        for contact in contacts:
            data_list.append(contact)

        res["data"] = data_list

        res["curPage"] = pageIndex

        res['success'] = True
        # print(res['data'])
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 每个月的加班情况 列表
class OverViewConfirmView(LoginRequiredMixin, View):
    '''将加班状态改成 以签核'''

    def post(self, request):
        # print(request.POST)
        res = {}
        apply_id = request.POST.get('id')
        if len(apply_id) != 0:
            data = ApplyList.objects.get(id=apply_id)
            data.applyState = 2
            data.confirmTime = datetime.datetime.now()
            data.confirmUser = request.user.name
            data.save()
            res['result'] = True
        else:
            res['result'] = False

        if res['result']:
            year = request.GET.get('year').lstrip()
            month = request.GET.get('month')
            time = year + '-' + month

            #  获取今天的日期  # 2019-09-11
            today = datetime.date.today().strftime('%Y-%m')
            print(time)
            # 如果提报的是本月的加班，拒绝的话，将上个月提报的状态 改成 已经签核
            if time == str(today):
                ApplyList.objects.filter(applyUser=request.user.username, applyState=3, fk_month__month=today).update(
                    applyState=5)
            print(today)

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


#  总览加班
class OverViewFusedView(LoginRequiredMixin, View):
    '''将加班状态 改为 已拒绝'''

    def post(self, request):
        res = {}
        apply_Id = request.POST.get('id')
        if len(apply_Id) != 0:
            # print(apply_Id)
            fused = ApplyList.objects.get(id=apply_Id)
            fused.applyState = 4
            fused.confirmTime = datetime.datetime.now()
            fused.confirmUser = request.user.name
            fused.save()
            res['result'] = True
        else:
            res['result'] = False

        if res['result']:
            # print(111)
            year = request.GET.get('year').lstrip()
            month = request.GET.get('month')
            time = year + '-' + month

            #  获取今天的日期  # 2019-09-11
            today = datetime.date.today().strftime('%Y-%m')
            # print(time)
            # 如果提报的是本月的加班，拒绝的话，将上个月提报的状态 改成 已经签核
            if time == str(today):
                ApplyList.objects.filter(applyUser=request.user.username, applyState=3, fk_month__month=today).update(
                    applyState=2)
            # print(today)

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 一键确认加班
class OverViewAllConfirmView(LoginRequiredMixin, View):
    def post(self, request):
        res = {}
        # data = list(request.POST.get('data[]'))
        id = dict(request.POST)

        if len(id) != 0:
            data = id['data[]']
            for app_id in data:
                app = ApplyList.objects.get(id=int(app_id))
                app.applyState = 2
                app.confirmTime = datetime.datetime.now()
                app.confirmUser = request.user.name
                app.save()

            year = request.GET.get('year').lstrip()
            month = request.GET.get('month')
            time = year + '-' + month

            #  获取今天的日期  # 2019-09-11
            today = datetime.date.today().strftime('%Y-%m')
            # print(time)
            # 如果提报的是本月的加班，拒绝的话，将上个月提报的状态 改成 已经签核
            if time == str(today):
                ApplyList.objects.filter(applyUser=request.user.username, applyState=3, fk_month__month=today).update(
                    applyState=5)
            # print(today)
            res['result'] = True
        else:
            res['result'] = False

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 加班导出
class OverViewExport(LoginRequiredMixin, View):
    def get(self, request):
        # res = dict(result=False)
        year = request.GET.get('year')
        moth = request.GET.get('moth')
        addDate = year + '-' + moth
        # print(addDate)
        fields = ['username__username', 'username__name', 'data_time', 'data_hour', 'add_content']

        data = list(AddTime.objects.filter(fk_apply__applyState=2, fk_apply__fk_month__month=addDate,
                                           fk_apply__applyType=3).values(*fields).order_by('data_time'))
        result = json.dumps(data)
        # print(result)
        # print(type(result))

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=OvertimeProposeModel_V2.0.xls'

        output = addTime_report(result)
        output.seek(0)
        response.write(output.getvalue())
        # res['result'] = True
        # res['response'] = response
        return response

        # return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 请假导出
class AbnormalExport(LoginRequiredMixin, View):
    def get(self, request):
        time = request.GET.get('time')
        # print(time)
        time = time.split(' - ')
        fields = ['username__username', 'username__name', 'leave_type', 'startTime', 'endTime', 'leave_start_time',
                  'leave_end_time',
                  'time_start_period', 'time_end_period', 'agent_worknum', 'reason']
        # 假如时间采用区间的方式，用如下方式进行处理  时间格式转化 datetime.datetime.strptime(request.GET.get('StartDate'), "%m/%d/%Y")
        # res['apply'].currRecDate = datetime.strptime(res['apply'].currRecDate, '%Y-%m-%d %H:%M:%S.%f')
        # DATE_FORMAT(inTime, '%%Y-%%m-%%d %%H:%%i:%%s')
        # CusQuestions.objects.filter(crt_tm__range=["2017-06-14", "2017-06-15"])
        # print(time)

        if time[0] == time[1]:
            data = list(
                Abnormal.objects.filter(fk_apply__applyType=1, fk_apply__applyDate=time[0]).values(*fields))
            # print('111', data)
        else:
            data = time[1]
            da = str(int(data[len(data) - 1]) + 1)
            aft_time = data.replace(data[len(data) - 1], da)
            data = list(
                Abnormal.objects.filter(fk_apply__applyType=1, fk_apply__applyDate__range=[time[0], aft_time]).values(
                    *fields))
            # print('222', data)

        result = json.dumps(data)
        # print(result)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=LeaveFormModel.xls'

        output = abnormal_report(result)
        output.seek(0)
        # print(output.seek(0))
        response.write(output.getvalue())
        return response


# 异常导出
class AbsentExport(LoginRequiredMixin, View):
    def get(self, request):
        time = request.GET.get('time')
        time = time.split(' - ')
        fields = ['username__username', 'username__name', 'startTime', 'time_end_period', 'card_type', 'absent_type',
                  'reason']
        # 假如时间采用区间的方式，用如下方式进行处理  时间格式转化 datetime.datetime.strptime(request.GET.get('StartDate'), "%m/%d/%Y")
        # res['apply'].currRecDate = datetime.strptime(res['apply'].currRecDate, '%Y-%m-%d %H:%M:%S.%f')
        # DATE_FORMAT(inTime, '%%Y-%%m-%%d %%H:%%i:%%s')
        # CusQuestions.objects.filter(crt_tm__range=["2017-06-14", "2017-06-15"])
        if time[0] == time[1]:
            data = list(
                Absent.objects.filter(fk_apply__applyType=2, fk_apply__applyDate=time[0]).values(*fields))
        else:
            data = list(Absent.objects.filter(fk_apply__applyType=2, fk_apply__applyDate__range=time).values(*fields))
        result = json.dumps(data)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=ExceptionBackForm.xls'

        output = absent_report(result)
        output.seek(0)
        # print(output.seek(0))
        response.write(output.getvalue())
        return response
