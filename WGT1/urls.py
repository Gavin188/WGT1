"""WGT1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from WGT1 import settings
from dqe.views import DqeView
from system.views_user import LoginView, LogoutView, IndexView
from testManage import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 登录
    path('', IndexView.as_view(), name='index'),
    path('', DqeView.as_view(), name='wgtLogin'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # 系统管理
    path('system/', include('system.urls', namespace='system')),

    # 机台和配件的申请和处理
    path('dqe/', include('dqe.urls', namespace='dqe')),

    # 加班 - 异常 - 请假 提报
    path('dqe/overtime/', include('overtime.urls', namespace='overtime')),

    # 测试管理
    path('dqe/testManage/', include('testManage.urls', namespace='testManage')),

]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    ]
