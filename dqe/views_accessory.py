import datetime
import json

import pandas as pd
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from dqe.models import Project, Stage, Fused, ApplyList, ApplyListDetail, AccessoryListDetail
from system.mixin import LoginRequiredMixin
from system.models import Menu, Access


# 庫存界面
# @method_decorator(login_required, name='dispatch') #测试3
class AccessoryView(LoginRequiredMixin, View):  # class InventoryView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict()
        fields = ['ftype', 'fname']
        # 平台
        projects = Project.objects.all()
        res['projects'] = projects

        # 階段
        stages = Stage.objects.all()
        res['stages'] = stages

        # 版本
        fuseds = Fused.objects.all()
        res['fuseds'] = fuseds
        # 配件
        access = Access.objects.all()
        res['access'] = access

        # 机台版本狀態
        applyState_list = []
        for applyState in Fused.STATE_TYPE:
            applyState_dict = dict(key=applyState[0], value=applyState[1])
            applyState_list.append(applyState_dict)
        res['applyState_list'] = applyState_list

        timeState_list = []
        for timeState in Fused.TIME_TYPE:
            timeState_dict = dict(key=timeState[0], value=timeState[1])
            timeState_list.append(timeState_dict)
        res['timeState_list'] = timeState_list

        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)

        return render(request, 'dqe/Accessory/accessory.html', res)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=

    def post(self, request):

        res = dict(result=False)
        # # 申请单 生成  获取页面的数值  保存到申请单中
        data = request.POST
        data = dict(data)
        # 添加到申请单中
        # 创建一个申请单  申请单号设定为 申请部门 向 确认部门 申请时间

        if len(data) == 8:
            # if data['example_length']:
            #     del data['example_length']
            del data['csrfmiddlewaretoken']
            data = pd.DataFrame(data)
            da = data['qty']

            qty_arr = []
            for i in da:
                qty_arr.append(i)

            for i in qty_arr:
                if i.isdigit() and int(i) > 0:
                    res['result'] = True

                else:
                    res['result'] = False
                    break

            if res['result'] == True:
                apply = ApplyList()
                apply.applyNum = str(request.user.username) + "-" + 'Ipad' + "-" + str(
                    datetime.datetime.now().strftime('%Y%m%d_%H%M'))
                apply.applyUser = request.user.name
                apply.applyUnit = request.user.department  # 申請單位
                apply.applyDate = datetime.datetime.now()
                apply.applyState = 1  # ("1", "待簽核"), ("2", "已簽核")
                apply.applyName = 1  # ('1', 'ipad'),('2','配件')
                apply.save()

                for i in range(len(data)):
                    ApplyListDetail.objects.create(
                        fk_apply=apply,
                        # fk_project=Project.objects.get(pname=data.loc[i, 'platform']),
                        # fk_stage=Stage.objects.get(sname=data.loc[i, 'hw_build']),
                        # fk_fused=Fused.objects.get(fname=data.loc[i, 'fused']),
                        platform=data.loc[i, 'platform'],
                        stage=data.loc[i, 'hw_build'],
                        type=data.loc[i, 'fused'],
                        model=str(data.loc[i, 'model']),
                        timeState=str(data.loc[i, 'timeState']),
                        qty=str(data.loc[i, 'qty']),
                        comments=str(data.loc[i, 'comments']),
                        applyDate=datetime.datetime.now(),
                    )

                # res['result'] = True
        else:
            res['result'] = False
        return HttpResponse(json.dumps(res), content_type='application/json')


class AccessoryListView(LoginRequiredMixin, View):
    '''配件申请'''

    def post(self, request):
        res = dict(result=False)
        # # 申请单 生成  获取页面的数值  保存到申请单中
        data = request.POST
        data = dict(data)
        # 添加到申请单中
        # 创建一个申请单  申请单号设定为 申请部门 向 确认部门 申请时间

        if len(data) == 6:
            del data['csrfmiddlewaretoken']
            data = pd.DataFrame(data)
            da = data['qty1']

            qty_arr = []
            for i in da:
                qty_arr.append(i)

            for i in qty_arr:
                if i.isdigit() and int(i) > 0:
                    res['result'] = True

                else:
                    res['result'] = False
                    break

            if res['result'] == True:
                apply = ApplyList()
                apply.applyNum = str(request.user.username) + "-" + '配件' + "-" + str(
                    datetime.datetime.now().strftime('%Y%m%d_%H%M'))
                apply.applyUser = request.user.name
                apply.applyUnit = request.user.department  # 申請單位
                apply.applyDate = datetime.datetime.now()
                apply.applyState = 1  # ("1", "待簽核"), ("2", "已簽核")
                apply.applyName = 2
                apply.save()
                for i in range(len(data)):
                    AccessoryListDetail.objects.create(
                        fk_apply=apply,
                        accessory=data.loc[i, 'accessory'],
                        stage=data.loc[i, 'hw_build'],
                        timeState=str(data.loc[i, 'timeState']),
                        qty=str(data.loc[i, 'qty1']),
                        comments=str(data.loc[i, 'comments']),
                        applyDate=datetime.datetime.now()

                    )

        else:
            res['result'] = False
        return HttpResponse(json.dumps(res), content_type='application/json')
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++==
