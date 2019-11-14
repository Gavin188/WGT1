import datetime
import json

from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views import View

from dqe.models import ApplyList, ApplyListDetail
from system.forms import UEditorTestModelForm
from system.mixin import LoginRequiredMixin
from testManage.models import TestFun, TaskArrange, TimeArrange
from testManage.tests import dynamicUpdateObjFields


class CurrentTestView(LoginRequiredMixin, View):
    '''今日测试首页'''

    def get(self, request):
        user = request.user
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        errmsg = ''
        arrange = list(
            TaskArrange.objects.filter(tester=user, task_date__pub_date=str(time)).values('comments').distinct())
        if arrange:
            comments = []
            for i in arrange:
                if i['comments'] not in comments:
                    comments.append(i['comments'])
            print(comments)

            context = {
                'comments': comments,
                # 'errmsg': errmsg,
            }

        else:
            context = {
                'arrange': '今日还没有上传测试任务',
                'errmsg': errmsg
            }
        return render(request, 'testManage/CurrentTest.html', context)


class CurrentTestListView(LoginRequiredMixin, View):
    '''今日测试首页 列表'''

    def post(self, request):
        res = {"success": "",
               "totalRows": "",
               "curPage": "",
               "data": " ", }
        today = datetime.date.today()
        # print('854584684--', today)
        # 获取 测试项
        comments = request.POST.get('comments')
        # 获取 案例管理 - 测试项
        data = list(TestFun.objects.filter(fk_case__function=comments).values())

        print('---', data)

        # 分页
        count = len(data)
        pageIndex = request.POST.get('curPage')
        pageSize = request.POST.get('pageSize')
        pageInator = Paginator(data, pageSize)
        contacts = pageInator.page(pageIndex)
        data_list = []  # 最终返回的结果集合
        for contact in contacts:
            data_list.append(contact)
        res['data'] = data_list
        res['success'] = True
        res['totalRows'] = count
        res['curPage'] = pageIndex
        # print(res)
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class TestWordView(LoginRequiredMixin, View):
    '''今日测试 - 显示 测试说明'''

    def get(self, request):
        # 获取显示测试项
        title = request.GET.get('title')
        # 页面显示的内容
        form = UEditorTestModelForm(
            initial={'Description': '请输入：',
                     'title': title}
        )
        # 上传的前端
        context = {
            'form': form,
        }
        return render(request, 'system/Test_Word/UpdateWord.html', context)

    def post(self, request):
        # 获取前端传来的数据，放入model中
        form = UEditorTestModelForm(request.POST)
        if form.is_valid():
            form.save()
            # print('OK')
            return HttpResponse(u"上传成功！")
        else:
            return HttpResponse(u"数据校验错误")


class CurrentUpdView(LoginRequiredMixin, View):
    '''今日测试  - 保存数据'''

    def post(self, request):
        res = dict(result=False)
        # 获取 修改的数据
        id = request.POST.get('id')
        test_results = request.POST.get('test_results')
        radar_id = request.POST.get('radar_id')
        comments = request.POST.get('comments')

        # 获取前端的ID 连接数据库
        try:
            test = TestFun.objects.get(id=id)
        except Exception:
            res['result'] = False
            return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
        # 如果修改了function 则保存，一下同理
        if test_results != '[object Object]':
            dynamicUpdateObjFields(obj=test, fieldName='test_results',
                                   fieldValue=str(test_results))
            res['result'] = True
        if radar_id != '[object Object]':
            dynamicUpdateObjFields(obj=test, fieldName='radar_id',
                                   fieldValue=str(radar_id))
            res['result'] = True
        if comments != '[object Object]':
            dynamicUpdateObjFields(obj=test, fieldName='comments',
                                   fieldValue=str(comments))
            res['result'] = True

        if res['result']:
            today = datetime.date.today()
            try:
                time_arrange = TimeArrange.objects.get(pub_date=today)
            except Exception:
                time_arrange = TimeArrange()
                time_arrange.pub_date = today
                time_arrange.save()

            test.fk_time = time_arrange
            test.save()

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


class CurrentApplyView(LoginRequiredMixin, View):
    '''首页显示 今日测试 一键申请'''

    def get(self, request):
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        message = True
        fields = ['wgt_no', 'serial_no', 'fused', 'nand', 'test_build', 'comments', 'state']
        ipad_list = list(TaskArrange.objects.filter(task_date__pub_date=str(time), tester=request.user).values(*fields))
        # 判断今日的数据是否上传
        if len(ipad_list) == 0:
            message = False

        context = {
            'ipads': ipad_list,
            'message': message,
        }
        return render(request, 'testManage/CurrentApply.html', context)

    def post(self, request):
        '''
        2 、判断 一键申请，是否已经申请
        '''
        res = dict(result=False)
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        fields = ['wgt_no', 'serial_no', 'fused', 'nand', 'test_build', 'comments', 'state']
        ipad_list = list(TaskArrange.objects.filter(task_date__pub_date=str(time), tester=request.user).values(*fields))
        # 判断 状态 是否已经申请
        # state_list = [i['state'] for i in ipad_list]
        # if '2' in state_list:
        #     message = '你已经申请了'
        #     res['message'] = message
        #     res['result'] = False
        #     return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')

        apply = ApplyList()
        apply.applyNum = str(request.user.username) + "-" + 'Ipad' + "-" + str(
            datetime.datetime.now().strftime('%Y%m%d_%H%M'))
        apply.applyUser = request.user.name
        apply.applyUnit = request.user.department  # 申請單位
        apply.applyDate = datetime.datetime.now()
        apply.applyState = 1  # ("1", "待簽核"), ("2", "已簽核")
        apply.applyName = 1  # ('1', 'ipad'),('2','配件')
        apply.save()
        try:
            for ipad in ipad_list:
                detail = ApplyListDetail()
                detail.fk_apply = apply
                detail.sn = ipad['serial_no']
                detail.qty = '1'
                detail.timeState = '一天'
                detail.comments = ipad['comments']
                detail.applyDate = datetime.datetime.now()
                detail.save()
                res['result'] = True

                TaskArrange.objects.filter(task_date__pub_date=str(time), tester=request.user).update(
                    state='2')
        except Exception as e:
            message = '申请失败'
            res['message'] = message
            res['result'] = False

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
