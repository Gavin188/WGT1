from django.urls import path
from .views import SystemView
from . import views_structure, views_user, views_menu, views_role

from django.conf.urls import url

import system.views_project as views_project
import system.views_stage as views_stage
import system.views_notice as views_notice

import system.views_prodtype as views_prodtype

app_name = 'system'

urlpatterns = [
    path('', SystemView.as_view(), name='login'),

    path('basic/structure/', views_structure.StructureView.as_view(), name='basic-structure'),
    path('basic/structure/create/', views_structure.StructureCreateView.as_view(), name='basic-structure-create'),
    path('basic/structure/list/', views_structure.StructureListView.as_view(), name='basic-structure-list'),
    path('basic/structure/delete/', views_structure.StructureDeleteView.as_view(), name='basic-structure-delete'),
    path('basic/structure/add_user/', views_structure.Structure2UserView.as_view(), name='basic-structure-add_user'),

    path('basic/user/', views_user.UserView.as_view(), name='basic-user'),
    path('basic/user/list/', views_user.UserListView.as_view(), name='basic-user-list'),
    path('basic/user/create/', views_user.UserCreateView.as_view(), name='basic-user-create'),
    path('basic/user/detail/', views_user.UserDetailView.as_view(), name='basic-user-detail'),
    path('basic/user/user_info/', views_user.UserInfoView.as_view(), name='basic-user-user_info'),
    path('basic/user/passwordchange/', views_user.PasswdChangeView.as_view(), name='basic-passwordchange'),
    path('basic/user/update/', views_user.UserUpdateView.as_view(), name='basic-user-update'),
    path('basic/user/password_change/', views_user.PasswordChangeView.as_view(), name='basic-user-password_change'),
    path('basic/user/delete/', views_user.UserDeleteView.as_view(), name='basic-user-delete'),
    path('basic/user/enable/', views_user.UserEnableView.as_view(), name='basic-user-enable'),
    path('basic/user/disable/', views_user.UserDisableView.as_view(), name='basic-user-disable'),


    path('rbac/menu/', views_menu.MenuListView.as_view(), name='rbac-menu'),
    path('rbac/menu/create/', views_menu.MenuCreateView.as_view(), name='rbac-menu-create'),
    path('rbac/menu/update/', views_menu.MenuUpdateView.as_view(), name='rbac-menu-update'),

    path('rbac/role/', views_role.RoleView.as_view(), name='rbac-role'),
    path('rbac/role/create/', views_role.RoleCreateView.as_view(), name='rbac-role-create'),
    path('rbac/role/list/', views_role.RoleListView.as_view(), name='rbac-role-list'),
    path('rbac/role/update/', views_role.RoleUpdateView.as_view(), name='rbac-role-update'),
    path('rbac/role/delete/', views_role.RoleDeleteView.as_view(), name='rbac-role-delete'),
    path('rbac/role/role2user/', views_role.Role2UserView.as_view(), name="rbac-role-role2user"),
    path('rbac/role/role2menu/', views_role.Role2MenuView.as_view(), name="rbac-role-role2menu"),
    path('rbac/role/role2menu_list/', views_role.Role2MenuListView.as_view(), name="rbac-role-role2menu_list"),

    # 专案
    url(r'^basic/project/$', views_project.ProjectView.as_view(), name='basic-project'),
    url(r'^basic/project/list$', views_project.ProjectListView.as_view(), name='basic-project-list'),
    url(r'^basic/project/update$', views_project.ProjectUpdateView.as_view(), name='basic-project-update'),
    url(r'^basic/project/delete$', views_project.ProjectDeleteView.as_view(), name='basic-project-delete'),

    # 阶段
    url(r'^basic/stage/$', views_stage.StageView.as_view(), name='basic-stage'),
    url(r'^basic/stage/list$', views_stage.StageListView.as_view(), name='basic-stage-list'),
    url(r'^basic/stage/update$', views_stage.StageUpdateView.as_view(), name='basic-stage-update'),
    url(r'^basic/stage/delete$', views_stage.StageDeleteView.as_view(), name='basic-stage-delete'),

    # 专案 和 阶段 联动
    url(r'^basic/project/stage$', views_stage.ProjectAndStageLinkageView.as_view(), name='basic-project-stage'),

    # 公告表 Notice
    url(r'^basic/notice/$', views_notice.NoticeView.as_view(), name='basic-notice'),
    url(r'^basic/notice/list$', views_notice.NoticeListView.as_view(), name='basic-notice-list'),
    url(r'^basic/notice/update$', views_notice.NoticeUpdateView.as_view(), name='basic-notice-update'),
    url(r'^basic/notice/delete$', views_notice.NoticeDeleteView.as_view(), name='basic-notice-delete'),

    # 产品类别表 ProductType
    url(r'^basic/prodtype/$', views_prodtype.ProductTypeView.as_view(), name='basic-prodtype'),
    url(r'^basic/prodtype/list$', views_prodtype.ProductTypeListView.as_view(), name='basic-prodtype-list'),
    url(r'^basic/prodtype/update$', views_prodtype.ProductTypeUpdateView.as_view(), name='basic-prodtype-update'),
    url(r'^basic/prodtype/delete$', views_prodtype.ProductTypeDeleteView.as_view(), name='basic-prodtype-delete'),

]