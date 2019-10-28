from django.urls import path
from django.conf.urls import url
from django.urls import path
import dqe.views_applydetail as views_applydetail
import dqe.views_borrowapply as views_borrowapply
import dqe.views_inventory as views_inventory
import dqe.views_loanconfirm as views_loanconfirm
import dqe.views_oct as views_oct
from dqe import views_accessory
from dqe.views import DqeView

app_name = 'dqe'

urlpatterns = [
    path('', DqeView.as_view(), name='ucsLogin'),
    # +————————————————————机台库存——————————————————————
    url(r'^inventory/$', views_inventory.InventoryView.as_view(), name='inventory'),
    url(r'^inventory/list$', views_inventory.InventoryListView.as_view(), name='inventory-list'),
    url(r'^inventory/update$', views_inventory.InventoryUpdateView.as_view(), name='inventory-update'),
    url(r'^inventory/delete$', views_inventory.InventoryDeleteView.as_view(), name='inventory-delete'),
    url(r'^inventory/onedelete$', views_inventory.InventoryoneDeleteView.as_view(), name='inventory-onedelete'),
    # @Gavin 新增机台
    url(r'^inventory/insert$', views_inventory.InventoryInsertView.as_view(), name='inventory-insert'),

    # @Gavin  查询sn
    url(r'^order/selectByOrderId$', views_inventory.InventoryselectByOrderIdView.as_view(),
        name='inventory-selectByOrderId'),

    # ------------
    # url(r'^inventory/detail$', views_inventory.InventoryDetailView.as_view(), name='inventory-detail'), #机台详情
    # url(r'^inventory/out$', views_inventory.InventoryOutView.as_view(), name='inventory-out'),  # 出庫
    # url(r'^inventory/in$', views_inventory.InventoryInView.as_view(), name='inventory-in'),  # 入庫

    # ---------————————————————配件库存————————————————————————--------
    # 点击 借入申请确认 > 弹出一个界面，用于显示勾选的机台 OperateCacheTable
    url(r'^oct/$', views_oct.OperateCacheTableView.as_view(), name='oct'),
    url(r'^oct/list$', views_oct.OperateCacheTableListView.as_view(), name='oct-list'),
    url(r'^oct/update$', views_oct.OperateCacheTableUpdateView.as_view(), name='oct-update'),
    url(r'^oct/delete$', views_oct.OperateCacheTableDeleteView.as_view(), name='oct-delete'),
    url(r'^oct/onedelete$', views_oct.AccessoryDeleteView.as_view(), name='oct-onedelete'),
    url(r'^oct/selectByOrderId$', views_oct.AcceselectByOrderIdView.as_view(), name='oct-selectByOrderId'),

    # ----------------物料申请--------------------
    # @Gavin   一键申请   机台申请
    url(r'^accessoryinventory/$', views_accessory.AccessoryView.as_view(), name='accessory'),
    # @Gavin 一键申请    配件
    url(r'^accessoryinventory/list$', views_accessory.AccessoryListView.as_view(), name='accessory-list'),

    # todo:申请单详情
    url(r'^mt/applydetail/$', views_applydetail.ApplyDetailView.as_view(), name='mt-applydetail'),
    url(r'^mt/applydetail/list$', views_applydetail.ApplyDetailListView.as_view(), name='mt-applydetail-list'),

    # @Gavin 删除申请单
    url(r'^mt/applydetail/delete$', views_applydetail.ApplyDetailDeleteView.as_view(), name='mt-applydetail-delete'),

    # @Gavin  iPad 申请的详细信息
    url(r'^mt/applylist/detail$', views_applydetail.ApplyIPadDetailView.as_view(), name='mt-applyIpad-detail'),

    # Gavin ipad 申请iPad 详细信息列表
    url(r'^mt/applylistdetail/list$', views_applydetail.ApplyIpadListView.as_view(), name='mt-applyipad-list'),

    # @Gavin  配件 申请的详细信息
    url(r'^mt/accesslist/detail$', views_applydetail.ApplyAccessDetailView.as_view(), name='mt-ApplyAccess-detail'),

    # Gavin ipad 申请配件详细信息列表
    url(r'^mt/accessdetail/list$', views_applydetail.AccesssoryView.as_view(), name='mt-accesssorycount-list'),

    # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # todo: 借入申请
    url(r'^mt/borrowapply/$', views_borrowapply.BorrowApplyView.as_view(), name='mt-borrowapply'),
    url(r'^mt/borrowapply/list$', views_borrowapply.BorrowApplyListView.as_view(), name='mt-borrowapply-list'),
    # url(r'^mt/borrowapply/detail$', views_borrowapply.BorrowApplyDetailView.as_view(), name='mt-borrowapply-detail'),
    # 删除申请单
    url(r'^mt/borrowapply/delete$', views_borrowapply.BorrowApplyDeleteView.as_view(), name='mt-borrowapply-delete'),

    # @Gavin 修改IPad 申请详情单
    url(r'^mt/applydetail/update$', views_applydetail.ApplyDetailUpdateView.as_view(), name='mt-applydetail-update'),

    # @Gavin 修改配件 申请详情单
    url(r'^mt/borrowaccess/update$', views_applydetail.BorrowAccessUpdateView.as_view(), name='mt-borrowaccess-update'),

    # @Gavin 删除IPad申请详情单
    url(r'^mt/applydetailid/delete$', views_applydetail.ApplyDetailDelIdView.as_view(), name='mt-applydetailid-delete'),

    # @Gavin 删除配件申请详情单
    url(r'^mt/borrowaccess/delete$', views_applydetail.BorrowAccessDelView.as_view(), name='mt-borrowaccess-delete'),

    #  全部退还机台
    url(r'^mt/borrowapply/return$', views_borrowapply.BorrowApplyReturnView.as_view(), name='mt-borrowapply-retuen'),

    #  全部退还配件
    url(r'^mt/borrowwgtapply/return$', views_borrowapply.BorrowWGTReturnView.as_view(), name='mt-borrowwgt-retuen'),

    # ipad临时库存
    url(r'^mt/borrowipad/list$', views_loanconfirm.LoanIpadDetailListView.as_view(), name='mt-borrowipad-list'),

    # @Gavin 配件临时表
    url(r'^mt/borrowaccess/list$', views_loanconfirm.LoanAccessDetailView.as_view(), name='mt-borrowaccess-list'),

    # ------------------------------------------------------------------------------------------------------------------
    # todo:借出确认  loan confirm
    url(r'^mt/loanconfirm/$', views_loanconfirm.LoanConfirmView.as_view(), name='mt-loanconfirm'),
    # @Gavin 显示 申请单  借ipad or 配件
    url(r'^mt/loanconfirm/list$', views_loanconfirm.LoanConfirmListView.as_view(), name='mt-loanconfirm-list'),
    # @Gavin iPad 申请单详情表
    url(r'^mt/loanconfirm/detail$', views_loanconfirm.LoanConfirmDetailView.as_view(), name='mt-loanconfirm-detail'),
    # @Gavin 显示 用户申请单详细信息 ，显示需要机台机台
    url(r'^mt/loanconfirmdetail/list$', views_loanconfirm.LoanConfirmDetailListView.as_view(),
        name='mt-loanconfirmdetail-list'),

    # @Gavin 仓管借出iPad机台  将机台保存到 Oper table中
    url(r'^mt/loanipaddetail/list$', views_loanconfirm.LoanIpadDetailListView.as_view(),
        name='mt-loanipaddetail-list'),
    #  @Gavin 扫码 临时表 添加sn
    url(r'^mt/inventory/scanApply$', views_inventory.InventoryScanApplyView.as_view(), name='mt-inventory-scanApply'),
    # @Gavin  ipad 申请详情中 手动输入 wgt_no 编号
    url(r'^mt/inventory/handApply$', views_inventory.InventoryHandApplyView.as_view(), name='mt-inventory-handApply'),
    # @gavin 扫码还机台
    url(r'^mt/inventory/scanReturn$', views_inventory.InventoryScanReturnView.as_view(),
        name='mt-inventory-scanReturn'),

    # @Gavin 配件 申请单详情表
    url(r'^mt/loanconfirmaccess/detail$', views_loanconfirm.LoanConfirmAccessView.as_view(),
        name='mt-loanconfirmaccess-detail'),
    # @Gavin 显示 用户申请单详细信息 ，显示需要几个配件
    url(r'^mt/loanconfirmaccess/list$', views_loanconfirm.LoanConfirmAcessListView.as_view(),
        name='mt-loanconfirmaccess-list'),
    # @Gavin 借出配件 仓管借出配件  将机台保存到 Oper table中
    url(r'^mt/loanaccessdetail/list$', views_loanconfirm.LoanAccessDetailView.as_view(),
        name='mt-loanaccessdetail-list'),
    # @Gavin  配件 申请单中 手动输入 wgt_no 编号
    url(r'^mt/handApply$', views_loanconfirm.loanHandApplyView.as_view(), name='loanconfirm-handApply'),

    # @Gavin  配件 申请单中 联想 wgt_no 编号
    url(r'^mt/rearchwgt$', views_loanconfirm.loanRearchWGTView.as_view(), name='loanconfirm-rearchwgt'),
    # -------------------

    # iPad确认借出
    # @Gavin  将申请的机台 状态 改为已经借出， 并将 申请的状态改为 以签核
    url(r'^mt/loanconfirmipadlist/confirm$', views_loanconfirm.LoanConfirmIpadList.as_view(),
        name='mt-loanconfirmipadlist-confirm'),
    # @Gavin  将申请的机台多余的删除
    url(r'^mt/loanipad/delete$', views_loanconfirm.LoanIpadDeleteView.as_view(), name='mt-loanipad-delete'),
    # @Gavin 选择机台退还
    url(r'^mt/loanconfirmdetail/return$', views_loanconfirm.LoanConfirmReturnIpadView.as_view(),
        name='mt-loanconfirmdetail-return'),
    # --------------
    # 配件 确认借出
    # @Gavin 将申请的配件 状态 改为已经借出 ， 并将申请的状态 改为 已经签核
    url(r'^mt/loanconfirmaccesslist/confirm$', views_loanconfirm.LoanConfirmAccessList.as_view(),
        name='mt-loanconfirmaccesslist-confirm'),
    # @Gavin  将申请的配件多余的删除
    url(r'^mt/loanaccess/delete$', views_loanconfirm.LoanAccessDeleteView.as_view(), name='mt-loanaccess-delete'),
    # @Gavin 选择机台退还
    url(r'^mt/loanaccess/return$', views_loanconfirm.LoanConfirmReturnAccessView.as_view(),
        name='mt-loanaccess-return'),
    # @Gavin 填写sn 归还机台
    url(r'^mt/loanaccess/hand$', views_loanconfirm.LoanAccessReturnView.as_view(), name='mt-Loanaccess-hand'),

    # message
    url(r'^mt/loanconfirm/message$', views_loanconfirm.LoanConfirmMessageView.as_view(), name='mt-loanconfirm-message'),

    # # 機台出入時間分析  Outdated warning
    # url(r'^is/OutdateWarn/$', views_ow.OutdateWarnView.as_view(), name='is-outdatedWarning'),
    # url(r'^is/OutdateWarn/list$', views_ow.OutdateWarnListView.as_view(), name='is-outdatedWarning-list'),

    # 邮件功能
    # url(r'^is/machineStatusQuery/reset$', tasks.OvertimeDetect.as_view(), name='is-machineStatusQuery-reset'),

    # # Reset记录
    # url(r'^is/machineStatusQuery/reset/list$', views_msq.MachineStatusQueryResetListView.as_view(),
    #     name='is-machineStatusQuery-reset-list'),
    # # information search
    # # 机台状态查询  Machine Status Query
    # url(r'^is/machineStatusQuery/$', views_msq.MachineStatusQueryView.as_view(), name='is-machineStatusQuery'),
    # url(r'^is/abnormal/list$', views_msq.AbnormalListView.as_view(), name='ov-abnormal-list'),
    # url(r'^is/machineStatusQuery/list$', views_msq.MachineStatusQueryListView.as_view(),
    #     name='is-machineStatusQuery-list'),
    # url(r'^is/machineStatusQuery/detail$', views_msq.MachineStatusQueryDetailView.as_view(),
    #     name='is-machineStatusQuery-detail'),
    # # 机台状态查询详情：列表
    # url(r'^is/machineStatusQuery/detail/list$', views_msq.MachineStatusQueryDetailListView.as_view(),
    #     name='is-machineStatusQuery-detail-list'),
]
