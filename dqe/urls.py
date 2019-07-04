from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import url

import dqe.views_inventory as views_inventory
import dqe.views_applydetail as views_applydetail
import dqe.views_oct as views_oct
import dqe.views_apply as views_apply
import dqe.views_borrowapply as views_borrowapply
import dqe.views_loanconfirm as views_loanconfirm
import dqe.views_msq as views_msq
import dqe.views_ow as views_ow
from dqe import views
from dqe.views import DqeView, calendarView

import dqe.tasks as tasks

app_name = 'dqe'

urlpatterns = [
    # path('', PersonalView.as_view(), name='login'),
    path('', DqeView.as_view(), name='ucsLogin'),
    path('', DqeView.as_view(), name='ucsLogin'),
    path('calendar/', calendarView.as_view(), name='calendar'),

    # 机台入库  Inventory Manager
    # url(r'^inventory/$', login_required(views_inventory.InventoryView.as_view()), name='inventory'),    #测试1：通过装饰器实现LoginRequiredMixin相同功能
    url(r'^inventory/$', views_inventory.InventoryView.as_view(), name='inventory'),
    url(r'^inventory/list$', views_inventory.InventoryListView.as_view(), name='inventory-list'),
    url(r'^inventory/update$', views_inventory.InventoryUpdateView.as_view(), name='inventory-update'),
    url(r'^inventory/delete$', views_inventory.InventoryDeleteView.as_view(), name='inventory-delete'),
    url(r'^inventory/detail$', views_inventory.InventoryDetailView.as_view(), name='inventory-detail'),
    url(r'^inventory/detail/list$', views_inventory.InventoryDetailListView.as_view(), name='inventory-detail-list'),
    url(r'^inventory/out$', views_inventory.InventoryOutView.as_view(), name='inventory-out'),  # 出庫
    url(r'^inventory/in$', views_inventory.InventoryInView.as_view(), name='inventory-in'),  # 入庫

    # 将选择的机台放入购物车  称之为 OperateCacheTable
    url(r'^inventory/addToShopping$', views_inventory.InventoryAddToShoppingView.as_view(),
        name='inventory-addToShopping'),

    # 扫码 申请
    url(r'^inventory/scanApply$', views_inventory.InventoryScanApplyView.as_view(), name='inventory-scanApply'),

    url(r'^inventory/scanReturn$', views_inventory.InventoryScanReturnView.as_view(), name='inventory-scanReturn'),

    # 点击 借入申请确认 > 弹出一个界面，用于显示勾选的机台 OperateCacheTable
    url(r'^oct/$', views_oct.OperateCacheTableView.as_view(), name='oct'),
    url(r'^oct/list$', views_oct.OperateCacheTableListView.as_view(), name='oct-list'),
    url(r'^oct/update$', views_oct.OperateCacheTableUpdateView.as_view(), name='oct-update'),
    url(r'^oct/delete$', views_oct.OperateCacheTableDeleteView.as_view(), name='oct-delete'),
    url(r'^oct/applyConfirm$', views_oct.ApplyConfirmView.as_view(), name='oct-applyConfirm'),

    # 申请单  Machine Transfer
    url(r'^mt/apply/$', views_apply.ApplyView.as_view(), name='mt-apply'),
    url(r'^mt/apply/list$', views_apply.ApplyListView.as_view(), name='mt-apply-list'),
    url(r'^mt/apply/update$', views_apply.ApplyUpdateView.as_view(), name='mt-apply-update'),
    url(r'^mt/apply/delete$', views_apply.ApplyDeleteView.as_view(), name='mt-apply-delete'),
    url(r'^mt/apply/detail$', views_apply.ApplyDetailView.as_view(), name='mt-apply-detail'),

    # 申请详情
    url(r'^mt/applydetail/$', views_applydetail.ApplyDetailView.as_view(), name='mt-applydetail'),
    url(r'^mt/applydetail/list$', views_applydetail.ApplyDetailListView.as_view(), name='mt-applydetail-list'),
    url(r'^mt/applydetail/update$', views_applydetail.ApplyDetailUpdateView.as_view(), name='mt-applydetail-update'),
    url(r'^mt/applydetail/delete$', views_applydetail.ApplyDetailDeleteView.as_view(), name='mt-applydetail-delete'),

    # 借入申请
    url(r'^mt/borrowapply/$', views_borrowapply.BorrowApplyView.as_view(), name='mt-borrowapply'),
    url(r'^mt/borrowapply/list$', views_borrowapply.BorrowApplyListView.as_view(), name='mt-borrowapply-list'),
    url(r'^mt/borrowapply/detail$', views_borrowapply.BorrowApplyDetailView.as_view(), name='mt-borrowapply-detail'),
    url(r'^mt/borrowapply/delete$', views_borrowapply.BorrowApplyDeleteView.as_view(), name='mt-borrowapply-delete'),
    url(r'^mt/borrowapplydetail/list$', views_borrowapply.BorrowApplyDetailListView.as_view(),
        name='mt-borrowapplydetail-list'),

    # 借出确认  loan confirm
    url(r'^mt/loanconfirm/$', views_loanconfirm.LoanConfirmView.as_view(), name='mt-loanconfirm'),
    url(r'^mt/loanconfirm/list$', views_loanconfirm.LoanConfirmListView.as_view(), name='mt-loanconfirm-list'),

    url(r'^mt/loanconfirm/detail$', views_loanconfirm.LoanConfirmDetailView.as_view(), name='mt-loanconfirm-detail'),
    url(r'^mt/loanconfirmdetail/list$', views_loanconfirm.LoanConfirmDetailListView.as_view(),
        name='mt-loanconfirmdetail-list'),
    # lc 就是 loanconfirm的缩写   ApplyRemark 就是 调增Remark的信息表单信息
    url(r'^mt/loanconfirm/aremark$', views_loanconfirm.LoanConfirmAremarkView.as_view(), name='mt-loanconfirm-aremark'),
    # LoanConfirm_Detail.html中 詳情：機台確認借出
    url(r'^mt/loanconfirmdetail/machremark$', views_loanconfirm.LoanConfirmMachRemarkView.as_view(),
        name='mt-loanconfirmdetail-machremark'),
    # LoanConfirm_Detail.html中 新增备注 +
    url(r'^mt/loanconfirmdetail/addremark$', views_loanconfirm.LoanConfirmAddRemarkView.as_view(),
        name='mt-loanconfirmdetail-addremark'),

    # message
    url(r'^mt/loanconfirm/message$', views_loanconfirm.LoanConfirmMessageView.as_view(), name='mt-loanconfirm-message'),

    # information search
    # 机台状态查询  Machine Status Query
    url(r'^is/machineStatusQuery/$', views_msq.MachineStatusQueryView.as_view(), name='is-machineStatusQuery'),
    url(r'^is/machineStatusQuery/list$', views_msq.MachineStatusQueryListView.as_view(),
        name='is-machineStatusQuery-list'),
    url(r'^is/machineStatusQuery/detail$', views_msq.MachineStatusQueryDetailView.as_view(),
        name='is-machineStatusQuery-detail'),
    # 机台状态查询详情：列表
    url(r'^is/machineStatusQuery/detail/list$', views_msq.MachineStatusQueryDetailListView.as_view(),
        name='is-machineStatusQuery-detail-list'),

    # 機台出入時間分析  Outdated warning
    url(r'^is/OutdateWarn/$', views_ow.OutdateWarnView.as_view(), name='is-outdatedWarning'),
    url(r'^is/OutdateWarn/list$', views_ow.OutdateWarnListView.as_view(), name='is-outdatedWarning-list'),

    # 邮件功能
    url(r'^is/machineStatusQuery/reset$', tasks.OvertimeDetect.as_view(), name='is-machineStatusQuery-reset'),

    # Reset记录
    url(r'^is/machineStatusQuery/reset/list$', views_msq.MachineStatusQueryResetListView.as_view(),
        name='is-machineStatusQuery-reset-list'),

]
