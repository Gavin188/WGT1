from django.conf.urls import url
from django.urls import path

from overtime import views_abnormal, views_apply, views_absent, views_addtime
from overtime.views import calendarView

app_name = 'overtime'

urlpatterns = [
    # path('', PersonalView.as_view(), name='login'),
    # path('', DqeView.as_view(), name='ucsLogin'),
    # path('', DqeView.as_view(), name='ucsLogin'),
    path('calendar/', calendarView.as_view(), name='calendar'),

    # @Gavin 异常  申请
    url(r'^ov/abnormal/list$', views_abnormal.AbnormalListView.as_view(), name='ov-abnormal-list'),
    # @Gavin  请假 申请
    url(r'^ov/absent/list$', views_absent.AbsentListView.as_view(), name='ov-absent-list'),

    # -------普通用户申请单-------------
    # @Gavin 加班和异常请假申请详情
    url(r'^ov/apply/list$', views_apply.ApplyListView.as_view(), name='ov-apply-list'),
    # @Gavin 申请单列表
    url(r'^ov/apply/detail$', views_apply.ApplyDetailView.as_view(), name='ov-apply-detail'),
    # @Gavin 删除申请单
    url(r'^ov/apply/delete$', views_apply.ApplyDeleteView.as_view(), name='ov-apply-delete'),
    # @Gavin 查看请假申请单详情
    url(r'^ov/applyabnormal/detail$', views_apply.ApplyAbnormalView.as_view(), name='ov-applyAbnormal-detail'),

    # @Gavin 查看请假申请单详情列表
    url(r'^ov/applyabnormalist/detail$', views_apply.ApplyAbnormalistView.as_view(), name='ov-applyAbnormalist-detail'),

    # @Gavin 查看异常申请单详情
    url(r'^ov/applyabsent/detail$', views_apply.ApplyAbsentView.as_view(), name='ov-applyAbsent-detail'),

    # @Gavin 查看异常申请单详情列表
    url(r'^ov/applyabsentlist/detail$', views_apply.ApplyAbsentlistView.as_view(), name='ov-applyAbsentlist-detail'),

    # @Gavin 查看加班申请详情
    url(r'^ov/applyaddtime/detail$', views_apply.ApplyAddTimeView.as_view(), name='ov-applyAddTime-detail'),
    # @Gavin 查看加班申请详情列表
    url(r'^ov/applyaddtimelist/detail$', views_apply.ApplyAddTimelistView.as_view(), name='ov-applyAddTimelist-detail'),

    # message
    url(r'^ov/overtime/message$', views_apply.OvertimeMessageView.as_view(), name='mt-overtime-message'),

    # ------------主管看的请假和异常加班申请单----------------------------
    # @Gavin 加班和异常请假申请详情
    url(r'^ov/applyleader/list$', views_apply.ApplyLeaderListView.as_view(), name='ov-applyleader-list'),
    # @Gavin 申请单列表
    url(r'^ov/applyleader/detail$', views_apply.ApplyLeaderDetailView.as_view(), name='ov-applyleader-detail'),

    # @Gavin 删除申请单
    url(r'^ov/applyleader/delete$', views_apply.ApplyLeaderDeleteView.as_view(), name='ov-applyleader-delete'),
    # @Gavin 查看请假申请单详情
    url(r'^ov/applyleaderabnormal/detail$', views_apply.ApplyLeaderAbnormalView.as_view(),
        name='ov-applyleaderAbnormal-detail'),

    # @Gavin 查看请假申请单详情列表
    url(r'^ov/applyleaderabnormalist/detail$', views_apply.ApplyLeaderAbnormalistView.as_view(),
        name='ov-applyleaderAbnormalist-detail'),

    # @Gavin 查看异常申请单详情
    url(r'^ov/applyleaderabsent/detail$', views_apply.ApplyLeaderAbsentView.as_view(),
        name='ov-applyleaderAbsent-detail'),

    # @Gavin 查看异常申请单详情列表
    url(r'^ov/applyleaderabsentlist/detail$', views_apply.ApplyLeaderAbsentlistView.as_view(),
        name='ov-applyleaderAbsentlist-detail'),

    # @Gavin 查看加班申请单详情
    url(r'^ov/applyleaderaddtime/detail$', views_apply.ApplyLeaderAddTimeView.as_view(),
        name='ov-applyleaderAddTime-detail'),

    # @Gavin 查看加班申请单详情列表
    url(r'^ov/applyleaderaddtimelist/detail$', views_apply.ApplyLeaderAddTimelistView.as_view(),
        name='ov-applyleaderaddtimelist-detail'),

    # ---------------主管确认申请单-------------------------------------------
    # @Gavin 确认申请单
    url(r'^ov/apply/confirm$', views_apply.ApplyConfirmView.as_view(), name='ov-apply-confirm'),
    # @Gavin 拒绝请假
    url(r'^ov/apply/refuse$', views_apply.ApplyRefuseView.as_view(), name='ov-apply-refuse'),

    # -------------------@Gavin 加班申请-------------
    # @Gavin 加班提报
    url(r'^ov/time/list$', views_addtime.TimeListView.as_view(), name='ov-time-list'),

    # @Gavin 总览加班详情
    url(r'^ov/overviewtime/detail$', views_addtime.OverViewDetail.as_view(), name='ov-overviewtime-detail'),

    # @Gavin 总览加班详情 - 导出
    url(r'^ov/overviewtime/export$', views_addtime.OverViewExport.as_view(), name='ov-overviewtime-export'),

    # @Gavin 总览加班每个月加班情况
    url(r'^ov/overviewmonth/list$', views_addtime.OverViewMonthListView.as_view(), name='ov-overviewmonth-list'),

    # @Gavin 总览加班详情 确认---
    url(r'^ov/overviewconfirm/list$', views_addtime.OverViewConfirmView.as_view(), name='ov-overviewconfirm-list'),
    # @Gavin 总览加班详情 拒绝---
    url(r'^ov/overviewfused/detail$', views_addtime.OverViewFusedView.as_view(), name='ov-overviewfused-detail'),

    # @Gavin   一键确认加班
    url(r'^ov/overviewallconfirm/list$', views_addtime.OverViewAllConfirmView.as_view(),
        name='ov-overviewallconfirm-list'),

    # 请假导出
    # @Gavin 请假加班 - 导出
    url(r'^ov/applyabnormal/export$', views_addtime.AbnormalExport.as_view(), name='ov-applyabnormal-export'),
    # @Gavin 异常加班 - 导出
    url(r'^ov/applyabsent/export$', views_addtime.AbsentExport.as_view(), name='ov-applyabsent-export'),





]
