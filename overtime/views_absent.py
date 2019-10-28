import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from overtime.models import ApplyList
from overtime.forms import AbnormalCreateForm, AbsentCreateForm
from system.mixin import LoginRequiredMixin
from system.models import Menu, UserProfile


# 异常申请
class AbsentListView(LoginRequiredMixin, View):
    def get(self, request):
        res = {}
        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)
        return render(request, 'overtime/Absent/absentlist.html', res)

    def post(self, request):
        res = dict(result=False)
        user_id = request.POST.get('id')
        user = UserProfile.objects.get(id=user_id)
        absent_create_from = AbsentCreateForm(request.POST)
        apply_num = str(request.user.name) + '-' + '异常' + '-' + str(datetime.datetime.now().strftime('%Y%m%d_%H%M'))
        if absent_create_from.is_valid():
            applyList = ApplyList()
            applyList.applyUser = request.user.username
            applyList.applyUnit = request.user.department  # 申請單位
            applyList.applyDate = datetime.datetime.now()
            applyList.applyNum = apply_num
            applyList.applyState = 1  # ("1", "待簽核"), ("2", "已簽核"),("3","已取消")
            applyList.applyType = 2  # ('1', '请假'),('2','异常'),("3","加班")
            applyList.save()

            absent = absent_create_from.save(commit=False)
            absent.username = user
            absent.fk_apply = applyList
            absent.save()
            res['result'] = True
        else:
            res['result'] = False
        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type="application/json")
