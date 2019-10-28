from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import View

from dqe.models import ApplyList
from system.mixin import LoginRequiredMixin
from system.models import Structure, Menu


# # 庫存界面
# class ApplyView(LoginRequiredMixin, View):
#     def get(self, request):
#         res = dict(data=ApplyList.objects.all())
#
#         # 部門
#         structures = Structure.objects.all()
#         res['structures'] = structures
#
#         # 申請單狀態
#         applyState_list = []
#         for applyState in ApplyList.APPLYSTATE_TYPE:
#             applyState_dict = dict(key=applyState[0], value=applyState[1])
#             applyState_list.append(applyState_dict)
#         res['applyState_list'] = applyState_list
#         menu = Menu.get_menu_by_request_url(url=self.request.path_info)
#         if menu is not None:
#             res.update(menu)
#
#         return render(request, 'dqe/Apply/Apply_List.html', res)


# # 庫存列表
# class ApplyListView(LoginRequiredMixin, View):
#     def get(self, request):
#         fields = ['id', 'applyNum', 'applyUser', 'applyUnit', 'applyDate', 'applyTime', 'applyState',
#                   'applydetail__confirmUser', 'applydetail__lendDate', 'applydetail__lendUnit', 'applydetail__lendtime',
#                   'applydetail__remark']
#         searchFields = ['applyDate', 'lendDate', 'applyUnit', 'lendUnit', 'applyUser', 'applyState']  # 与数据库字段一致
#         filters = {i + '__icontains': request.GET.get(i, '') for i in searchFields if
#                    i not in [''] and request.GET.get(i,
#                                                      '')}  # 此处的if语句有很大作用，如remark中数据为None,可通过if request.GET.get('')将传入为''的不将条件放入进去
#
#         # 假如时间采用区间的方式，用如下方式进行处理  时间格式转化 datetime.datetime.strptime(request.GET.get('StartDate'), "%m/%d/%Y")
#         # if request.GET.get('startapplyDate'):
#         #     filters['applyDate__gte'] = request.GET.get('startapplyDate')
#         # if request.GET.get('endapplyDate'):
#         #     filters['applyDate__lte'] = request.GET.get('endapplyDate')
#
#         # if request.GET.get('applyDate'):
#         #     filters['applyDate'] = request.GET.get('applyDate')
#         # if request.GET.get('lendDate'):
#         #     filters['lendDate'] = request.GET.get('lendDate')
#
#         # 查询Apply所有结果
#         #  alists = list(set(adlists))
#         # res = dict(data=list(Apply.objects.values(*fields)))
#         res = dict()
#         # #
#         adlists = Apply.objects.values_list('applyNum', flat=True)
#
#         # print(adlists)
#
#         alists = list(set(adlists))
#
#         print(alists)
#
#         filters['applyNum__in'] = alists
#
#         data = list(Apply.objects.filter(**filters).values(*fields).order_by('applyDate'))
#
#         res['data'] = data
#         print('res', res)
#
#         return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')


# # 庫存 新增 和 修改
# # get方式是跳转链接，而post方式是submit
# class ApplyUpdateView(LoginRequiredMixin, View):
#     # 注意：编辑页面中type=hidden隐藏的id，目的就是为了标识是编辑/增加操作
#     def get(self, request):
#         res = dict()
#         if 'id' in request.GET and request.GET['id']:
#             apply = get_object_or_404(Apply, pk=request.GET.get('id'))
#             res['apply'] = apply
#         else:
#             applys = Apply.objects.all()
#             res['applys'] = applys
#
#         # 部門
#         structures = Structure.objects.all()
#         res['structures'] = structures
#         # 申請單狀態
#         applyState_list = []
#         for applyState in Apply.APPLYSTATE_TYPE:
#             applyState_dict = dict(key=applyState[0], value=applyState[1])
#             applyState_list.append(applyState_dict)
#         res['applyState_list'] = applyState_list
#
#         return render(request, 'dqe/Apply/Apply_Update.html', res)
#
#     def post(self, request):
#         res = dict(result=False)
#         if 'id' in request.POST and request.POST['id']:  # id的存在，就是为了说明是新增数据还是编辑数据
#             apply = get_object_or_404(Apply, pk=request.POST.get('id'))
#         else:
#             apply = Apply()
#
#         apply_create_form = ApplyCreateForm(request.POST, instance=apply)
#
#         if apply_create_form.is_valid():
#             apply_create_form.save()
#             res['result'] = True
#
#         return HttpResponse(json.dumps(res), content_type='application/json')

#
# # 申請單删除
# class ApplyDeleteView(LoginRequiredMixin, View):
#     def post(self, request):
#         res = dict(result=False)
#         id = list(map(int, request.POST.get('id').split(',')))[0]
#
#         if 'id' in request.POST and request.POST['id']:
#             id_list = map(int, request.POST.get('id').split(','))
#             Apply.objects.filter(id__in=id_list).delete()
#             res['result'] = True
#
#         return HttpResponse(json.dumps(res), content_type='application/json')


# # 申請單詳情
# class ApplyDetailView(LoginRequiredMixin, View):
#     def get(self, request):
#         ret = dict()
#         if 'id' in request.GET and request.GET['id']:
#             apply = get_object_or_404(ApplyList, pk=request.GET.get('id'))
#
#         # applyDetail = ApplyDetail.objects.get(fk_apply_id=request.GET.get('id'))[0]
#
#         ret['apply'] = apply
#
#         return render(request, 'dqe/Apply/Apply_Detail.html', ret)
