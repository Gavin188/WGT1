from django.conf.urls import url

from testManage import views, views_case, views_current, views_bug

app_name = 'testManage'

urlpatterns = [

    #     今日测试
    url(r'^is/currenttest$', views_current.CurrentTestView.as_view(), name='is-currenttest'),

    url(r'^is/currenttestlist$', views_current.CurrentTestListView.as_view(), name='is-currenttest-list'),
    #     案例管理
    url(r'^is/casemanage$', views_case.CasemanageView.as_view(), name='is-casemanage'),

    url(r'^is/casemanagelist$', views_case.CasemanageListView.as_view(), name='is-casemanage-list'),
    #     任务安排
    url(r'^is/taskarrange$', views.TaskArrangeView.as_view(), name='is-taskarrange'),

    #     联想查询姓名
    url(r'^is/taskarrangerearch$', views.TaskArrangeRearchView.as_view(), name='is-taskarrange-rearch'),

    #     联想查询sn
    url(r'^is/taskarrangerearchwgt$', views.TaskArrangeRearchWGTView.as_view(), name='is-taskarrange-rearchwgt'),

    url(r'^is/taskarrangelist$', views.TaskArrangeListView.as_view(), name='is-taskarrange-list'),
    # 删除任务
    url(r'^is/taskarrangedelete$', views.TaskArrangeDeleteView.as_view(), name='is-taskarrange-delete'),

    # bug登记详情
    url(r'^bug/bugregister$', views_bug.BugRegisterView.as_view(), name='bug-bugregister'),
    # bug登记详情列表
    url(r'^bug/bugregisterlist$', views_bug.BugRegisterListView.as_view(), name='bug-bugregister-list'),
    # bug数据新增
    url(r'^bug/bugregistersave$', views_bug.BugRegisterSaveView.as_view(), name='bug-bugregister-save'),
    # bug数据修改
    url(r'^bug/bugregisterupdate$', views_bug.BugRegisterUpdateView.as_view(), name='bug-bugregister-update'),
    #  bug 数据删除
    url(r'^bug/bugregisterdelete$', views_bug.BugRegisterDeleteView.as_view(), name='bug-bugregister-delete'),

    #  bug 记录
    url(r'^bug/bugremark$', views_bug.BugRemarkView.as_view(), name='bug-bugremark'),

    url(r'^bug/bugremarklist$', views_bug.BugRemarkListView.as_view(), name='bug-bugremark-list'),

]
