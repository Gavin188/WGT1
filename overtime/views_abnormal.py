import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from overtime.models import ApplyList
from overtime.forms import AbnormalCreateForm
from system.mixin import LoginRequiredMixin
from system.models import Menu, UserProfile


class calendarView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'calendar.html', None)


# 异常申请
class AbnormalListView(LoginRequiredMixin, View):
    def get(self, request):
        res = {}
        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            res.update(menu)
        return render(request, 'overtime/Abnormal/abnormalist.html', res)

    def post(self, request):
        res = dict(result=False)
        user_id = request.POST.get('id')
        user = UserProfile.objects.get(id=user_id)
        abnormal_create_form = AbnormalCreateForm(request.POST)

        apply_num = str(request.user.name) + "-" + '请假' + "-" + str(
            datetime.datetime.now().strftime('%Y%m%d_%H%M'))
        if abnormal_create_form.is_valid():
            applyList = ApplyList()
            applyList.applyUser = request.user.username
            applyList.applyUnit = request.user.department  # 申請單位
            applyList.applyDate = datetime.datetime.now()
            applyList.applyNum = apply_num
            applyList.applyState = 1  # ("1", "待簽核"), ("2", "已簽核"),("3","已取消")
            applyList.applyType = 1  # ('1', '请假'),('2','异常'),("3","加班")
            applyList.save()

            abnormal = abnormal_create_form.save(commit=False)
            abnormal.username = user
            abnormal.fk_apply = applyList

            abnormal.save()
            res['result'] = True

        return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type='application/json')
