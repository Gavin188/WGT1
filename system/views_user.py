# @Time   : 2018/10/16 23:11
# @Author : RobbieHan
# @File   : views_user.py

import json
import re
import time

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.views.generic.base import View, TemplateView

from custom import BreadcrumbMixin
from system.models import Structure, UserProfile
from .forms import LoginForm, UserCreateForm, UserUpdateForm, PasswordChangeForm
from .mixin import LoginRequiredMixin
from .models import Role

User = get_user_model()


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'index.html')


class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            if 'username' in request.COOKIES:
                username = request.COOKIES.get('username')
            else:
                username = ''
            return render(request, 'system/users/login.html', {'username': username})
        else:
            return HttpResponseRedirect('/')

    def post(self, request):
        response = HttpResponse()
        redirect_to = request.GET.get('next', '/')
        login_form = LoginForm(request.POST)
        ret = dict(login_form=login_form)
        if login_form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response.set_cookie('username', user_name, max_age=7 * 24 * 3600)
                    return HttpResponseRedirect(redirect_to)
                else:
                    ret['msg'] = '用户未激活！'
            else:
                ret['msg'] = '用户名或密码错误！'
        else:
            ret['msg'] = '用户和密码不能为空！'
        return render(request, 'system/users/login.html', ret)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class UserView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
    template_name = 'system/users/user.html'


class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'name', 'gender', 'mobile', 'email', 'department__name', 'post', 'superior__name', 'is_active',
                  'worknum', 'level', 'username', 'time_control']
        filters = dict()
        if 'select' in request.GET and request.GET['select']:
            filters['is_active'] = request.GET['select']
        ret = dict(data=list(User.objects.filter(**filters).values(*fields)))
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserCreateView(LoginRequiredMixin, View):
    """
    添加用户
    """

    # <QueryDict: {'csrfmiddlewaretoken': ['urJmQCVsug73dida3cEnHZKhAEzfIHwnpmVYRSunUpp759Efb9KaEqlv0Y5kyoLz'], 'id': ['3'], 'user': ['save'],
    def get(self, request):
        users = User.objects.exclude(username='admin')
        structures = Structure.objects.values()
        roles = Role.objects.values()

        # 加班管控
        time_list = []
        for time_con in UserProfile.time_choices:
            time_dict = dict(key=time_con[0], value=time_con[1])
            time_list.append(time_dict)

        ret = {
            'users': users,
            'structures': structures,
            'roles': roles,
            'time': time_list,
        }
        return render(request, 'system/users/user_create.html', ret)

    def post(self, request):
        user_create_form = UserCreateForm(request.POST, request.FILES)

        file_obj = request.FILES.get('file')

        # file_name = 'media/image/' + request.POST.get('name') + '_' + str(int(time.time())) + '.' + \
        #             file_obj.name.split('.')[
        #                 -1]  # 构造文件名以及文件路径
        # print('2111', file_name[1:])

        if user_create_form.is_valid():
            new_user = user_create_form.save(commit=False)
            # print('22', user_create_form.cleaned_data)
            new_user.password = make_password(user_create_form.cleaned_data['password'])
            if 'file' in request.FILES:
                file_name = 'media/image/' + request.POST.get('name') + '_' + str(int(time.time())) + '.' + \
                            file_obj.name.split('.')[
                                -1]  # 构造文件名以及文件路径

                with open(file_name, 'wb+') as f:
                    f.write(file_obj.read())
                new_user.image = file_name[6:]
            new_user.save()
            user_create_form.save_m2m()

            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(user_create_form.errors)
            user_create_form_errors = re.findall(pattern, errors)
            ret = {
                'status': 'fail',
                'user_create_form_errors': user_create_form_errors[0]
            }
        print('ret--', ret)
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserDetailView(LoginRequiredMixin, View):

    def get(self, request):
        user = get_object_or_404(User, pk=int(request.GET['id']))
        users = User.objects.exclude(Q(id=int(request.GET['id'])) | Q(username='admin'))
        structures = Structure.objects.values()
        roles = Role.objects.values()
        user_roles = user.roles.values()
        # 加班管控
        time_list = []
        for time_con in UserProfile.time_choices:
            time_dict = dict(key=time_con[0], value=time_con[1])
            time_list.append(time_dict)
        ret = {
            'user': user,
            'structures': structures,
            'users': users,
            'roles': roles,
            'user_roles': user_roles,
            'time': time_list
        }
        return render(request, 'system/users/user_detail.html', ret)


class UserInfoView(LoginRequiredMixin, View):
    """
    个人中心：个人信息查看修改和修改
    """

    def get(self, request):
        return render(request, 'system/user_info/user_info.html')

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            file_obj = request.FILES.get('file')

            # # print('2111', file_name[6:])
            # print('equest.POST.get', request.POST.get('name'))

            user = get_object_or_404(User, pk=int(request.POST['id']))

            # print(request.POST)
            user.name = request.POST.get('name')
            user.gender = request.POST.get('gender')
            user.birthday = request.POST.get('birthday')
            user.username = request.POST.get('username')
            user.mobile = request.POST.get('mobile')
            user.email = request.POST.get('email')
            user.worknum = request.POST.get('worknum')
            # user.department = request.POST.get('department')
            user.post = request.POST.get('post')
            # user.superior = request.POST.get('superior')
            if 'file' in request.FILES:
                file_name = 'media/image/' + request.POST.get('name') + '_' + str(int(time.time())) + '.' + \
                            file_obj.name.split('.')[
                                -1]  # 构造文件名以及文件路径
                print('++++', file_name)
                with open(file_name, 'wb+') as f:
                    f.write(file_obj.read())
                user.image = file_name[6:]
            user.save()

            ret = {"status": "success"}
        else:
            ret = {"status": "fail"}
        return HttpResponse(json.dumps(ret), content_type="application/json")


class PasswdChangeView(LoginRequiredMixin, View):
    """
    登陆用户修改个人密码
    """

    def get(self, request):
        ret = dict()
        user = get_object_or_404(User, pk=int(request.user.id))
        ret['user'] = user
        return render(request, 'system/user_info/passwd-change.html', ret)

    def post(self, request):

        user = get_object_or_404(User, pk=int(request.user.id))
        form = AdminPasswdChangeForm(request.POST)
        if form.is_valid():
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(form.errors)
            admin_passwd_change_form_errors = re.findall(pattern, errors)
            ret = {
                'status': 'fail',
                'admin_passwd_change_form_errors': admin_passwd_change_form_errors[0]
            }
        return HttpResponse(json.dumps(ret), content_type='application/json')


class AdminPasswdChangeForm(forms.Form):
    """
    管理员用户修改用户列表中的用户密码
    """
    # def __init__(self, *args, **kwargs):
    #     super(AdminPasswdChangeForm, self).__init__(*args, **kwargs)

    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"密码不能为空"
        })

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"确认密码不能为空"
        })

    def clean(self):
        cleaned_data = super(AdminPasswdChangeForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")


class UserUpdateView(LoginRequiredMixin, View):

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            user = get_object_or_404(User, pk=int(request.POST['id']))
        else:
            user = get_object_or_404(User, pk=int(request.user.id))
        user_update_form = UserUpdateForm(request.POST, instance=user)
        if user_update_form.is_valid():
            user_update_form.save()
            ret = {"status": "success"}
        else:
            ret = {"status": "fail", "message": user_update_form.errors}
        return HttpResponse(json.dumps(ret), content_type="application/json")


class PasswordChangeView(LoginRequiredMixin, View):

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            user = get_object_or_404(User, pk=int(request.GET.get('id')))
            ret['user'] = user
        return render(request, 'system/users/passwd_change.html', ret)

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            user = get_object_or_404(User, pk=int(request.POST['id']))
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                new_password = request.POST['password']
                user.set_password(new_password)
                user.save()
                ret = {'status': 'success'}
            else:
                pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
                errors = str(form.errors)
                password_change_form_errors = re.findall(pattern, errors)
                ret = {
                    'status': 'fail',
                    'password_change_form_errors': password_change_form_errors[0]
                }
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserDeleteView(LoginRequiredMixin, View):
    """
    删除数据：支持删除单条记录和批量删除
    """

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            User.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserEnableView(LoginRequiredMixin, View):
    """
    启用用户：单个或批量启用
    """

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = User.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(is_active=False).update(is_active=True)
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserDisableView(LoginRequiredMixin, View):
    """
    启用用户：单个或批量启用
    """

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = User.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(is_active=True).update(is_active=False)
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')
