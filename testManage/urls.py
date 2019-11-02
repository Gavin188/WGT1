from django.conf.urls import url

from testManage import views, views_case, views_current, views_bug

app_name = 'testManage'

urlpatterns = [

    #     今日测试
    url(r'^is/currenttest$', views_current.CurrentTestView.as_view(), name='is-currenttest'),

    url(r'^is/currenttestlist/$', views_current.CurrentTestListView.as_view(), name='is-currenttest-list'),
    #     案例管理
    url(r'^is/casemanage$', views_case.CasemanageView.as_view(), name='is-casemanage'),

    url(r'^is/casemanagelist$', views_case.CasemanageListView.as_view(), name='is-casemanage-list'),

    # 新增 案例管理测试项
    url(r'^is/casemodel/insert$', views_case.CaseModelInsertView.as_view(), name='is-casemodel-insert'),

    # 案例管理 - 显示测试项的具体测试功能
    url(r'^is/casefind/list$', views_case.CaseFunFindView.as_view(), name='is-casefind-list'),

    # 案例管理 - 显示测试说明的测试文档
    url(r'^is/casedesc/list$', views_case.CaseDescIroView.as_view(), name='is-casedesc-list'),

    # 案例管理 - 测试具体功能显示
    url(r'^is/casefun/(?P<case_id>\d+)/$', views_case.CaseFunListView.as_view(), name='is-casefun-list'),

    # 案例管理 - 删除测试功能
    url(r'^is/casefun/delete$', views_case.CaseFunDelView.as_view(), name='is-casefun-delete'),



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
