import json
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import View

from dqe.models import ApplyList, ApplyListDetail, OperateCacheTable, AccessoryListDetail, AccessDetails, AccessTable
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu


# 借出确认 界面
class LoanConfirmView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(data=ApplyList.objects.all())

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

        return render(request, 'dqe/LoanConfirm/LoanConfirm_List.html', res)


# 借出确认 列表
class LoanConfirmListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'applyNum', 'applyName', 'applyUser', 'applyDate', 'applyUnit', 'applyState']
        # 与数据库字段一致
        searchFields = ['applyDate', 'applyUnit', 'applyUser', 'applyState']
        # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   i not in ['', ] and request.GET.get(i, '')}

        res = dict(data=list(ApplyList.objects.filter(**filters).values(*fields).order_by('-applyState')))

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 进入ipad申請單 詳情界面
class LoanConfirmDetailView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            apply = get_object_or_404(ApplyList, pk=request.GET.get('id'))
        ret['apply'] = apply

        return render(request, 'dqe/LoanConfirm/LoanConfirmIpad_Detail.html', ret)


#  进入配件 申请单 详情页面
class LoanConfirmAccessView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            apply = get_object_or_404(ApplyList, pk=request.GET.get('id'))
        ret['apply'] = apply

        return render(request, 'dqe/LoanConfirm/LoanConfirmAccess_Detail.html', ret)


# ipad 申请单详情列表
class LoanConfirmDetailListView(LoginRequiredMixin, View):
    # Ipad申请详情列表
    def get(self, request):
        fields = ['id', 'sn', 'machineState', 'lendUnit', 'qty',
                  'comments', 'model', 'timeState', 'platform',
                  'stage', 'type', 'fk_apply__applyUser', 'fk_apply__applyUnit',
                  'applyDate']
        searchFields = ['platform', 'machineState', ]
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        # 通过隐含传递的applyId，反向查出applydetail中所有对应该applyId的信息
        filters['fk_apply_id'] = request.GET.get('applyId')

        res = dict(
            data=list(ApplyListDetail.objects.filter(**filters).values(*fields).order_by('-fk_apply__applyDate')))
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 配件 申请单详情列表
class LoanConfirmAcessListView(LoginRequiredMixin, View):
    # 配件申请详情列表
    def get(self, request):
        fields = ['id', 'machineState', 'lendUnit', 'qty',
                  'comments', 'accessory', 'timeState',
                  'stage', 'fk_apply__applyUser', 'fk_apply__applyUnit',
                  'applyDate', 'lendDate']
        searchFields = ['platform', 'machineState', ]
        filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
                   request.GET.get(i, '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去

        # 通过隐含传递的applyId，反向查出applydetail中所有对应该applyId的信息
        filters['fk_apply_id'] = request.GET.get('applyId')

        res = dict(
            data=list(AccessoryListDetail.objects.filter(**filters).values(*fields).order_by('-fk_apply__applyDate')))
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


#  申请单 - 借出iPad的 信息
class LoanIpadDetailListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'fk_applylistdetail__id', 'fk_inventory__sn', 'fk_inventory__wgt_no', 'fk_inventory__platform',
                  'fk_inventory__hw_build',
                  'fk_inventory__model', 'fk_inventory__fused',
                  'fk_inventory__units_status', 'opeuser', 'fk_applylistdetail__lendDate',
                  'fk_applylistdetail__timeState', 'returnDate']
        filters = {}

        filters['fk_applylistdetail__fk_apply_id'] = request.GET.get('applyId')
        res = dict(
            data=list(
                OperateCacheTable.objects.filter(**filters).values(*fields)))
        # print('reere', res)
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# @Gavin  配件申请单 仓管将 配件信息 录入临时表中  OperateCacheTable 中 并显示在 页面上
class LoanAccessDetailView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'fk_accesslistdetail__id', 'fk_accessory__sn',
                  'fk_accessory__hw_build', 'fk_accessory__accessory',
                  'fk_accessory__config', 'fk_accessory__status',
                  'opeuser', 'fk_accesslistdetail__lendDate',
                  'fk_accesslistdetail__timeState', 'returnDate']
        filters = {}

        filters['fk_accesslistdetail__fk_apply_id'] = request.GET.get('applyId')
        res = dict(
            data=list(
                AccessTable.objects.filter(**filters).values(*fields)))
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# 将多余 录入 Ope 数据库的iPad 删除
class LoanIpadDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        # print('2', request.POST)
        # print('3', request.POST['id'])
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            data = OperateCacheTable.objects.filter(id__in=id_list)
            for i in data:
                i.fk_inventory.units_status = 1
                i.fk_inventory.save()
            # data.fk_inventory__units_status = 1
            # data.fk_inventory.save()
            data.delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


'''
1. 先获取 申请单的 单号 和 数量 
2. 获取临时机台表当前的 单号 和 数量
3. 将 1，2 进行相减 如果 差值都等于0 则申请单状态 改为确认
                       差值小于0  则提示少几台机台
                       差值da于0  则提示多几台机台
4 如果 申请详情单号的单号 都是确认 就将申请单的状态改为 签核             

'''


class LoanConfirmIpadList(LoginRequiredMixin, View):
    # 申请确认
    # 思路：创建Apply>将ApplyDetail也创建出来>清空操作缓存>库存中的状态变为被申请状态

    def post(self, request):
        res = dict()

        if 'id' in request.POST and request.POST['id']:
            count_id = []  # 获取申请单详情ID
            qty_list = []  # 获取申请单详情对应的数量
            current_list = []  # 当前申请机台的数量

            # # 获取 该申请单机台的数量：
            applydetail_id = request.POST.get('apply_id')
            # applydetail = ApplyListDetail.objects.get(id=applydetail_id)
            # qty = applydetail.qty
            # print('---', applydetail_id)
            # 将操作缓存表中的数据 加入 到applydetail
            id_list = map(int, request.POST.get('id').split(','))
            # print('id_list', id_list)

            octObjs = OperateCacheTable.objects.filter(id__in=id_list)

            qty_num = list(ApplyListDetail.objects.filter(fk_apply_id=applydetail_id).values('qty', 'id'))
            for i in qty_num:
                qty_list.append(i['qty'])
            for i in qty_num:
                count_id.append(i['id'])

            # print('qty_list--', qty_list)

            for oct in octObjs:
                # 申请提单时，改变库存中的状态 变为被申请即可，当确认该单时，那么当前使用部门、当前入库人、当前入库日期都要改
                # print(oct.fk_applylistdetail.qty)

                # # 由申请的机台表 -> 申请详情单 -> 查找出数量
                # if oct.fk_applylistdetail.qty not in qty_list:
                #     qty_list.append(oct.fk_applylistdetail.qty)

                # # 由申请的机台表 -> 申请详情单 -> 查找出ID
                # if oct.fk_applylistdetail.id not in count_id:
                #     count_id.append(oct.fk_applylistdetail.id)

                oct.fk_inventory.units_status = 2  # STATE_TYPE = (("1", "入庫"), ("2", "已借出"), ("3", "出库"), ("4", "损坏"), ("5", "被外借"))
                oct.fk_applylistdetail.lendDate = datetime.now()

                oct.fk_inventory.save()
                oct.fk_applylistdetail.save()
            qty_data = dict(zip(count_id, qty_list))
            '''
            计算一下每个作者的文章数（我们每个作者都导入的Article的篇数一样，所以下面的每个都一样）
                        Article.objects.all().values('author_id').annotate(count=Count('author')).values('author_id', 'count')
                        <QuerySet [{'count': 20, 'author_id': 1}, {'count': 20, 'author_id': 2}, {'count': 20, 'author_id': 4}]>
                        SELECT author_id, COUNT(author_id) AS count FROM blog_article GROUP BY author_id
            '''

            for i in count_id:
                num_list = OperateCacheTable.objects.filter(fk_applylistdetail_id=i,
                                                            fk_inventory__units_status=2).count()
                current_list.append(num_list)

            print('current_list-', current_list)
            current_data = dict(zip(count_id, current_list))
            print('current_data:', current_data)
            print('qty_data:', qty_data)

            for k in qty_data:
                for m in current_data:
                    if k == m:
                        num = int(qty_data[k]) - current_data[m]
                        # num_list.append(num)
                        res[k] = num
            count_sum = list(res.values())

            for k in res.keys():
                if int(res[k]) == 0:
                    applylistdetail = ApplyListDetail.objects.get(id=int(k))

                    applylistdetail.machineState = 2  # (("1", "未確認"), ("2", "確認"), ("3", "拒絕"),)
                    applylistdetail.save()

                    res[k] = '已经添加完成'
                elif int(res[k]) > 0:
                    res[k] = '机台数量少 ' + str(res[k])
                elif int(res[k]) < 0:
                    res[k] = '机台数量多 ' + str(abs(res[k]))

            # print('res--', res)

            # print('count_sum --', count_sum)

            # ------申请单状态 ("1", "待簽核"), ("2", "已簽核")
            status = OperateCacheTable.objects.filter(fk_applylistdetail__fk_apply_id=applydetail_id).values(
                'fk_applylistdetail__machineState').distinct()
            flag = True
            # print('status', status)
            for i in status:
                # print(i)
                if int(i['fk_applylistdetail__machineState']) == 1:
                    flag = False
                    break
            if flag:
                da = ApplyList.objects.get(id=applydetail_id)
                da.applyState = 2
                da.save()
            # print('flag-- ', flag)
            res['result'] = True
        else:
            res['result'] = False

        print(res)
        return HttpResponse(json.dumps(res), content_type='application/json')


'''
1. 先获取 申请单的 单号 和 数量 
2. 获取临时配件表当前的 单号 和 数量
3. 将 1，2 进行相减 如果 差值都等于0 则申请单状态 改为确认
                       差值小于0  则提示少几台配件
                       差值da于0  则提示多几台配件
4 如果 申请详情单号的单号 都是确认 就将申请单的状态改为 签核             

'''


class LoanConfirmAccessList(LoginRequiredMixin, View):
    def post(self, request):
        res = dict()

        if 'id' in request.POST and request.POST['id']:
            count_id = []  # 获取申请单详情ID
            qty_list = []  # 获取申请单详情对应的数量
            current_list = []  # 当前申请机台的数量

            # # 获取 该申请单机台的数量：
            applydetail_id = request.POST.get('apply_id')

            # 将操作缓存表中的数据 加入 到applydetail
            id_list = map(int, request.POST.get('id').split(','))
            # print('id_list', id_list)

            octObjs = AccessTable.objects.filter(id__in=id_list)

            qty_num = list(AccessoryListDetail.objects.filter(fk_apply_id=applydetail_id).values('qty', 'id'))
            for i in qty_num:
                qty_list.append(i['qty'])

            print('54545', qty_num)

            for i in qty_num:
                count_id.append(i['id'])

            print('qty_list--', qty_list)
            print('count_id--', count_id)

            for oct in octObjs:
                # 申请提单时，改变库存中的状态 变为被申请即可，当确认该单时，那么当前使用部门、当前入库人、当前入库日期都要改
                # 由申请的机台表 -> 申请详情单 -> 查找出ID
                # if oct.fk_accesslistdetail.id not in count_id:
                #     count_id.append(oct.fk_accesslistdetail.id)

                oct.fk_accessory.status = 1  # STATE_TYPE = (("1", "In Use"), ("2", "Disuse"), ("3", "Other"))
                oct.fk_accesslistdetail.lendDate = datetime.now()

                oct.fk_accessory.save()
                oct.fk_accesslistdetail.save()
            # 先求出 申请单中 数量和单号
            qty_data = dict(zip(count_id, qty_list))
            print('申请单中：', qty_data)
            for i in count_id:
                num_list = AccessTable.objects.filter(fk_accesslistdetail_id=i,
                                                      fk_accessory__status=1).count()
                current_list.append(num_list)

            # 再求出 当前临时表 数量和单号
            current_data = dict(zip(count_id, current_list))
            print('临时表中：', current_data)

            for k in qty_data:
                for m in current_data:
                    if k == m:
                        num = int(qty_data[k]) - current_data[m]
                        # num_list.append(num)
                        res[k] = num

            print('res--', res.keys())
            for k in res.keys():
                if int(res[k]) == 0:
                    applylistdetail = AccessoryListDetail.objects.get(id=int(k))

                    applylistdetail.machineState = 2  # (("1", "未確認"), ("2", "確認"), ("3", "拒絕"),)
                    applylistdetail.save()

                    res[k] = '已经添加完成'
                elif int(res[k]) > 0:
                    res[k] = '配件数量少 ' + str(res[k])
                elif int(res[k]) < 0:
                    res[k] = '配件数量多 ' + str(abs(res[k]))

            # ------申请单状态 ("1", "待簽核"), ("2", "已簽核")
            status = AccessTable.objects.filter(fk_accesslistdetail__fk_apply_id=applydetail_id).values(
                'fk_accesslistdetail__machineState').distinct()
            flag = True
            # print('status', status)
            for i in status:
                # print(i)
                if int(i['fk_accesslistdetail__machineState']) == 1:
                    flag = False
                    break
            if flag:
                da = ApplyList.objects.get(id=applydetail_id)
                da.applyState = 2
                da.save()
            # print('flag-- ', flag)
            res['result'] = True
        else:
            res['result'] = False

        print(res)
        return HttpResponse(json.dumps(res), content_type='application/json')


# 将多余 录入 Ope 数据库的配件 删除
class LoanAccessDeleteView(LoginRequiredMixin, View):

    def post(self, request):
        res = dict(result=False)
        # print('2', request.POST)
        # print('3', request.POST['id'])
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            data = AccessTable.objects.filter(id__in=id_list)
            print(']]]', data)
            for i in data:
                i.fk_accessory.status = 2
                i.fk_accessory.save()
            data.delete()
            res['result'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')


'''
两种还机台的方法：选择还机台 ，扫码还机台
1. 根据获取的id 将数据库查询出来
2。状态改为入库
3。如果申请单的中 sn 全部为入库     则申请单状态变为 3 以销毁

'''


# 选择退还机台
class LoanConfirmReturnIpadView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        apply_id = request.POST.get('apply_id')
        print('454545454545', apply_id)

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            data = OperateCacheTable.objects.filter(id__in=id_list)
            for id in data:
                print(id)
                id.fk_inventory.units_status = 1  # STATE_TYPE = (("1", "入庫"), ("2", "已借出"), ("3", "出库"), ("4", "损坏"), ("5", "被外借"))
                id.returnDate = datetime.now()

                id.fk_inventory.save()
                id.save()

            status = OperateCacheTable.objects.filter(fk_applylistdetail__fk_apply_id=apply_id).values(
                'fk_inventory__units_status').distinct()
            flag = True

            for i in status:
                if int(i['fk_inventory__units_status']) == 2:
                    flag = False
                    break
            if flag:
                da = ApplyList.objects.get(id=apply_id)
                da.applyState = 3
                da.save()
            res['result'] = True
            return HttpResponse(json.dumps(res), content_type='application/json')


# 选择退还配件
class LoanConfirmReturnAccessView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        apply_id = request.POST.get('apply_id')
        # print(apply_id)

        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST.get('id').split(','))
            data = AccessTable.objects.filter(id__in=id_list)
            # print('2323', data)
            for id in data:
                print(id)
                id.fk_accessory.status = 2  # STATE_TYPE = (("1", "In Use"), ("2", "Disuse"), ("3", "Other"))
                id.returnDate = datetime.now()

                id.fk_accessory.save()
                id.save()

            status = AccessTable.objects.filter(fk_accesslistdetail__fk_apply_id=apply_id).values(
                'fk_accessory__status').distinct()
            flag = True
            # 1 In use 借出  2 Disuse 入库
            for i in status:
                print(i)
                if int(i['fk_accessory__status']) == 1:
                    flag = False
                    break
            print('flag', flag)
            if flag:
                da = ApplyList.objects.get(id=apply_id)
                da.applyState = 3
                da.save()
            res['result'] = True
            return HttpResponse(json.dumps(res), content_type='application/json')


# @Gavin 填写 配件SN 归还配件
class LoanAccessReturnView(LoginRequiredMixin, View):
    def get(self, request):
        applyDetailId = request.GET.get('applyListDetailId')
        # app_list = AccessoryListDetail.objects.get(id=request.GET.get('applyListDetailId'))
        #
        # qty = app_list.qty

        return render(request, 'dqe/LoanConfirm/AccessReturn.html', {'applyDetailId': applyDetailId})

    def post(self, request):
        res = dict(result=False)
        sns = request.POST.get('sns').split('\r\n')
        print('sns', sns)

        apply_id = request.GET.get('id')
        print('4444', apply_id)
        data = list(AccessTable.objects.filter(fk_accesslistdetail__fk_apply_id=apply_id).values_list(
            'fk_accessory__sn'))
        all_sns = []

        for i in range(len(data)):
            all_sns.append(data[i][0])
        print('all_sns---', all_sns)
        invalidSn = []  # 无效的sn
        if request.user.department:
            for sn in sns:
                if sn in all_sns:
                    print('sn', sn)
                    data = AccessTable.objects.filter(fk_accessory__sn=sn)
                    for da in data:
                        print('data.fk_accessory.status--', da.fk_accessory.status)
                        da.fk_accessory.status = 2
                        da.returnDate = datetime.now()
                        da.fk_accessory.save()
                        da.save()
                else:
                    invalidSn.append(sn)
        if invalidSn:
            res['invalidSn'] = invalidSn
            res['result'] = 2
        else:
            res['invStateSN'] = '無'

            res['result'] = 1

        status = AccessTable.objects.filter(fk_accesslistdetail__fk_apply_id=apply_id).values(
            'fk_accessory__status').distinct()
        flag = True

        for i in status:
            if int(i['fk_accessory__status']) == 1:
                flag = False
                break

        print('444141414', flag)
        if flag:
            da = ApplyList.objects.get(id=apply_id)
            da.applyState = 3
            da.save()

        return HttpResponse(json.dumps(res), content_type='application/json')


# message铃铛
class LoanConfirmMessageView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict()

        # res = dict(data=list(Apply.objects.filter(applyState=1).values('applyState').annotate(count=Count('applyState').values('applyState','count')))) #.order_by('-属性')

        # 统计applyState为待签核的状态的数据
        # res['data'] = list(Apply.objects.filter(applyState=1,applydetail__lendUnit=request.user.department).values('id','applyState','applydetail__lendUnit').distinct().annotate(count=Count('applyState')).values('applyState','count'))

        count = ApplyList.objects.filter(applyState=1, applylistdetail__lendUnit=request.user.department).values('id',
                                                                                                                 'applyState',
                                                                                                                 'applylistdetail__lendUnit').distinct().count()

        count1 = ApplyList.objects.filter(applyState=1, accessorylistdetail__lendUnit=request.user.department).values(
            'id',
            'applyState',
            'accessorylistdetail__lendUnit').distinct().count()

        count = count + count1

        res['data'] = [{'applyState': '1', 'count': count, 'confirmUnit': '仓管'}]

        # 如果沒有待簽核的,把0传递过去
        if res['data'] == []:
            res['data'] = [{'applyState': '1', 'count': 0}]

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# @Gavin   配件申请单中 将 sn 手动输入到 OPer table 表中
class loanHandApplyView(LoginRequiredMixin, View):
    def get(self, request):
        applyDetailId = request.GET.get('applyListDetailId')  # 30   apply_id  21

        app_list = AccessoryListDetail.objects.get(id=request.GET.get('applyListDetailId'))

        qty = app_list.qty
        # print('applyDetailId===', applyDetailId)
        # apply_id = app_list.fk_apply_id

        return render(request, 'dqe/LoanConfirm/HandApply.html',
                      {'applyDetailId': applyDetailId, 'qty': qty})

    def post(self, request):
        res = dict(result=False)
        sns = request.POST.get('sns').split('\r\n')

        applydetail_id = request.GET.get('applydetailid')
        app_list = AccessoryListDetail.objects.get(id=applydetail_id)

        apply_id = app_list.fk_apply_id
        # print('222', apply_id)

        invState1SN = []  # 已经存在 配件的临时表 的的配件 SN
        invState2SN = []  # 已经IN use的配件 SN
        invState3SN = []  # 已经Other的配件 SN
        invStateSN = []  # 无效的sn

        invState4SN = []  # 已经存在 临时表的 sn
        data = list(AccessTable.objects.filter(fk_accesslistdetail__fk_apply__id=apply_id).values('fk_accessory__sn'))
        for i in data:
            invState4SN.append(i['fk_accessory__sn'])
        print('data --- ', invState4SN)

        # try:
        if request.user.department:
            for sn in sns:
                if sn not in invState4SN:
                    invobj = AccessDetails.objects.filter(sn=sn)
                    if invobj:
                        print('2', invobj)
                        print('3', invobj[0])
                        if invobj[0].status == '2':
                            AccessTable.objects.get_or_create(
                                fk_accessory=invobj[0],
                                fk_accesslistdetail=AccessoryListDetail.objects.get(
                                    id=request.GET.get('applydetailid')),
                                opeuser=request.user.name

                            )

                        else:
                            if invobj[0].status == '1':
                                invState2SN.append(sn)
                            elif invobj[0].status == '3':
                                invState3SN.append(sn)
                    else:
                        invStateSN.append(sn)
                else:
                    invState1SN.append(sn)
        print(invState2SN)
        print(invState3SN)
        print(invStateSN)
        print(invState1SN)
        #  2 表示异常， 1 表示成功
        if invState2SN or invStateSN or invState3SN or invState1SN:
            if invStateSN:
                res['inStateSN'] = invStateSN
            else:
                res['inStateSN'] = '无'
            if invState1SN:
                res['inState1SN'] = invState1SN
            else:
                res['inState1SN'] = '无'
            if invState2SN:
                res['inState2SN'] = invState2SN
            else:
                res['inState2SN'] = '无'
            if invState3SN:
                res['inState3SN'] = invState3SN
            else:
                res['inState3SN'] = '无'
            res['result'] = 2
        else:
            res['result'] = 1

        # except Exception as e:
        #     res['result'] = 3
        print('res---', res)
        return HttpResponse(json.dumps(res), content_type='application/json')


#  联想记忆法
class loanRearchWGTView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        accessory = request.POST.get('search')
        print(accessory)
        if accessory:
            wgt_nos = list(
                AccessDetails.objects.filter(accessory__icontains=accessory).values('accessory').distinct()[:33])

            wgt_nos = [i['accessory'] for i in wgt_nos]

            res['username'] = wgt_nos
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
