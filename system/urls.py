from django.conf.urls.static import static
from django.urls import path, include

from WGT1 import settings
from system import views_fused, views_access, views_daily
from .views import SystemView
from . import views_structure, views_user, views_menu, views_role

from django.conf.urls import url

import system.views_project as views_project
import system.views_stage as views_stage
import system.views_notice as views_notice

import system.views_prodtype as views_prodtype

import system.views_word as views_word

app_name = 'system'

urlpatterns = [
                  path('', SystemView.as_view(), name='login'),

                  path('basic/structure/', views_structure.StructureView.as_view(), name='basic-structure'),
                  path('basic/structure/create/', views_structure.StructureCreateView.as_view(),
                       name='basic-structure-create'),
                  path('basic/structure/list/', views_structure.StructureListView.as_view(),
                       name='basic-structure-list'),
                  path('basic/structure/delete/', views_structure.StructureDeleteView.as_view(),
                       name='basic-structure-delete'),
                  path('basic/structure/add_user/', views_structure.Structure2UserView.as_view(),
                       name='basic-structure-add_user'),

                  path('basic/user/', views_user.UserView.as_view(), name='basic-user'),
                  path('basic/user/list/', views_user.UserListView.as_view(), name='basic-user-list'),
                  path('basic/user/create/', views_user.UserCreateView.as_view(), name='basic-user-create'),
                  # path('basic/user/avatar/', views_user.UserAvatarView.as_view(), name='basic-user-avatar'),
                  path('basic/user/detail/', views_user.UserDetailView.as_view(), name='basic-user-detail'),
                  path('basic/user/user_info/', views_user.UserInfoView.as_view(), name='basic-user-user_info'),
                  path('basic/user/passwordchange/', views_user.PasswdChangeView.as_view(),
                       name='basic-passwordchange'),
                  path('basic/user/update/', views_user.UserUpdateView.as_view(), name='basic-user-update'),
                  path('basic/user/password_change/', views_user.PasswordChangeView.as_view(),
                       name='basic-user-password_change'),
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
                  path('rbac/role/role2menu_list/', views_role.Role2MenuListView.as_view(),
                       name="rbac-role-role2menu_list"),

                  # 专案
                  url(r'^basic/project/$', views_project.ProjectView.as_view(), name='basic-project'),
                  url(r'^basic/project/list$', views_project.ProjectListView.as_view(), name='basic-project-list'),
                  url(r'^basic/project/update$', views_project.ProjectUpdateView.as_view(),
                      name='basic-project-update'),
                  url(r'^basic/project/delete$', views_project.ProjectDeleteView.as_view(),
                      name='basic-project-delete'),

                  # 阶段
                  url(r'^basic/stage/$', views_stage.StageView.as_view(), name='basic-stage'),
                  url(r'^basic/stage/list$', views_stage.StageListView.as_view(), name='basic-stage-list'),
                  url(r'^basic/stage/update$', views_stage.StageUpdateView.as_view(), name='basic-stage-update'),
                  url(r'^basic/stage/delete$', views_stage.StageDeleteView.as_view(), name='basic-stage-delete'),

                  # 专案 和 阶段 联动
                  # url(r'^basic/project/stage$', views_stage.ProjectAndStageLinkageView.as_view(), name='basic-project-stage'),

                  # 公告表 Notice
                  url(r'^basic/notice/$', views_notice.NoticeView.as_view(), name='basic-notice'),
                  url(r'^basic/notice/list$', views_notice.NoticeListView.as_view(), name='basic-notice-list'),
                  url(r'^basic/notice/update$', views_notice.NoticeUpdateView.as_view(), name='basic-notice-update'),
                  url(r'^basic/notice/delete$', views_notice.NoticeDeleteView.as_view(), name='basic-notice-delete'),

                  # 产品类别表 ProductType
                  url(r'^basic/prodtype/$', views_prodtype.ProductTypeView.as_view(), name='basic-prodtype'),
                  url(r'^basic/prodtype/list$', views_prodtype.ProductTypeListView.as_view(),
                      name='basic-prodtype-list'),
                  url(r'^basic/prodtype/update$', views_prodtype.ProductTypeUpdateView.as_view(),
                      name='basic-prodtype-update'),
                  url(r'^basic/prodtype/delete$', views_prodtype.ProductTypeDeleteView.as_view(),
                      name='basic-prodtype-delete'),

                  # 版本类别表 ProductType 上线版 测试版
                  url(r'^basic/fused/$', views_fused.FusedView.as_view(), name='basic-fused'),
                  url(r'^basic/fused/list$', views_fused.FusedListView.as_view(), name='basic-fused-list'),
                  url(r'^basic/fused/update$', views_fused.FusedUpdateView.as_view(), name='basic-fused-update'),
                  url(r'^basic/fused/delete$', views_fused.FusedDeleteView.as_view(), name='basic-fused-delete'),

                  # 配件信息
                  url(r'^basic/access/$', views_access.AccessView.as_view(), name='basic-access'),
                  url(r'^basic/access/list$', views_access.AccessListView.as_view(), name='basic-access-list'),
                  url(r'^basic/access/update$', views_access.AccessUpdateView.as_view(), name='basic-access-update'),
                  url(r'^basic/access/delete$', views_access.AccessDeleteView.as_view(), name='basic-access-delete'),

                  # 富文本编辑器 保存 测试文档说明书
                  # path('ueditor/', include('DjangoUeditor.urls')),
                  url(r'^basic/word/$', views_word.WordView.as_view(), name='basic-test-word'),
                  url(r'^basic/word/list$', views_word.WordListView.as_view(), name='basic-word-list'),
                  url(r'^basic/word/update$', views_word.WordUpdateView.as_view(), name='basic-word-update'),
                  url(r'^basic/word/detail$', views_word.WordDetailView.as_view(), name='basic-word-detail'),
                  url(r'^basic/word/delete$', views_word.WordDeleteView.as_view(), name='basic-word-delete'),

                  # 上传首页 各种EXCEL表格    /system/daily/ver/
                  url(r'^daily/ver/$', views_daily.ExcelUpload.as_view(), name='daily-excel'),
                  # url(r'^daily/excel_handle/$', views_daily.ExcelUpload.as_view(), name='basic-ver'),
                  # url(r'^basic/access/list$', views_access.AccessListView.as_view(), name='basic-access-list'),
                  # url(r'^basic/access/update$', views_access.AccessUpdateView.as_view(), name='basic-access-update'),
                  # url(r'^basic/access/delete$', views_access.AccessDeleteView.as_view(), name='basic-access-delete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  ## 没有这一句无法显示上传的图片
