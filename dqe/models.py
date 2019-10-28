import django
from django.db import models


# 平台
class Project(models.Model):
    pname = models.CharField(max_length=30, verbose_name="專案名稱")

    class Meta:
        verbose_name = "测试平台"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pname


# 阶段表
class Stage(models.Model):
    sname = models.CharField(max_length=30, verbose_name="階段名稱")

    class Meta:
        verbose_name = "階段表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sname


# # 产品类别
# class ProductType(models.Model):
#     tname = models.CharField(max_length=30, default='54', verbose_name='加班时数')
#     tnumber = models.CharField(max_length=30, default='2', verbose_name='周加班次数')
#
#     class Meta:
#         verbose_name = '加班提报'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.tname

# 机台类型
class Fused(models.Model):
    STATE_TYPE = (('1', 'Wi-Fi'), ('2', 'Cellular'))
    TIME_TYPE = (('1', '一天'), ('2', '长借'))
    ftime = models.CharField(max_length=20, choices=TIME_TYPE, default="1", verbose_name="是否长借")
    ftype = models.CharField(max_length=20, choices=STATE_TYPE, default="1", verbose_name="机台类型")
    fname = models.CharField(max_length=30, verbose_name="版本类型")

    class Meta:
        verbose_name = "版本类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fname


# 申请单
class ApplyList(models.Model):
    APPLYSTATE_TYPE = (("1", "待簽核"), ("2", "已簽核"), ("3", "已销毁"))
    NAME_TYPE = (("1", "ipad"), ("2", "配件"))
    applyNum = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請單號", )
    applyUser = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請人", )
    applyUnit = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請單位", )
    applyDate = models.DateTimeField(auto_now_add=True, verbose_name='申請時間', )
    applyState = models.CharField(max_length=30, choices=APPLYSTATE_TYPE, default="1", blank=True,
                                  verbose_name="申請狀態", )
    applyName = models.CharField(max_length=30, choices=NAME_TYPE, default="1", blank=True,
                                 verbose_name="申請物品", )
    lendRemark = models.CharField(max_length=30, blank=True, null=True, verbose_name="借出單備註", )

    class Meta:
        verbose_name = "申請單"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.applyNum


# 申请单详情表 -- 与库存关联

class ApplyListDetail(models.Model):
    MACHINE_STATE = (("1", "未確認"), ("2", "確認"), ("3", "拒絕"),)
    fk_apply = models.ForeignKey(ApplyList, blank=True, null=True, on_delete=models.CASCADE, verbose_name="申請單號")
    machineState = models.CharField(max_length=30, choices=MACHINE_STATE, default="1", blank=True,
                                    verbose_name="機台確認狀態", )
    # confirmUser = models.CharField(max_length=30, blank=True, null=True, verbose_name="確認人", )
    lendDate = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name='确认時間', )
    applyDate = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name='申请时间', )
    lendUnit = models.CharField(max_length=30, blank=True, null=True, default='仓管', verbose_name="借出單位", )

    # fk_project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="测试平台")
    # fk_stage = models.ForeignKey(Stage, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="阶段")
    # fk_fused = models.ForeignKey(Fused, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="类型")
    platform = models.CharField(max_length=30, blank=True, null=True, verbose_name="测试平台")
    stage = models.CharField(max_length=30, blank=True, null=True, verbose_name="阶段")
    type = models.CharField(max_length=30, blank=True, null=True, verbose_name="类型")
    model = models.CharField(max_length=30, blank=True, null=True, verbose_name="机台类型", )
    timeState = models.CharField(max_length=30, blank=True, null=True, verbose_name="是否长借", )
    qty = models.TextField(blank=True, null=True, verbose_name="数量")
    comments = models.TextField(blank=True, null=True, verbose_name="機台備註")

    class Meta:
        verbose_name = "机台申請單详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_apply.applyNum


# 操作Ipad 临时緩存表
class OperateCacheTable(models.Model):
    fk_inventory = models.ForeignKey('IpadDetails', null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name="申請機台")

    fk_applylistdetail = models.ForeignKey('ApplyListDetail', null=True, blank=True, on_delete=models.CASCADE,
                                           verbose_name="Ipad申请单号")
    opeuser = models.CharField(max_length=30, null=True, blank=True, verbose_name="操作者", )
    returnDate = models.CharField(max_length=30, blank=True, null=True, verbose_name="退还时间", )

    class Meta:
        verbose_name = "Ipad临时申请表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_inventory.sn


# 配件申请详情单
class AccessoryListDetail(models.Model):
    MACHINE_STATE = (("1", "未確認"), ("2", "確認"), ("3", "拒絕"),)
    fk_apply = models.ForeignKey(ApplyList, blank=True, null=True, on_delete=models.CASCADE, verbose_name="申請單號")
    machineState = models.CharField(max_length=30, choices=MACHINE_STATE, default="1", blank=True,
                                    verbose_name="機台確認狀態", )

    lendDate = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name='确认時間', )
    applyDate = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name='申请时间', )

    lendUnit = models.CharField(max_length=30, blank=True, null=True, default='仓管', verbose_name="借出單位", )
    stage = models.CharField(max_length=30, blank=True, null=True, verbose_name="阶段")
    accessory = models.CharField(max_length=30, blank=True, null=True, verbose_name="配件")
    timeState = models.CharField(max_length=30, blank=True, null=True, verbose_name="是否长借", )
    qty = models.TextField(blank=True, null=True, verbose_name="数量")
    comments = models.TextField(blank=True, null=True, verbose_name="機台備註")

    class Meta:
        verbose_name = "配件申請單详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_apply.applyNum


# 操作配件临时緩存表
class AccessTable(models.Model):
    fk_accessory = models.ForeignKey('AccessDetails', null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name='申请配件')
    fk_accesslistdetail = models.ForeignKey('AccessoryListDetail', null=True, blank=True, on_delete=models.CASCADE,
                                            verbose_name="配件申请单号")
    opeuser = models.CharField(max_length=30, null=True, blank=True, verbose_name="操作者", )
    returnDate = models.CharField(max_length=30, blank=True, null=True, verbose_name="退还时间", )

    class Meta:
        verbose_name = "配件临时申请表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_accessory.sn


# Ipad 详情表
class IpadDetails(models.Model):
    STATE_TYPE = (("1", "入庫"), ("2", "已借出"), ("3", "出库"), ("4", "损坏"), ("5", "被外借"))
    platform = models.CharField(max_length=30, blank=True, null=True, verbose_name='测试平台')
    hw_build = models.CharField(max_length=30, blank=True, null=True, verbose_name='阶段')
    wgt_no = models.CharField(max_length=30, blank=True, null=True, verbose_name='wgt编号')
    sn = models.CharField(max_length=30, blank=True, null=True, verbose_name='机台SN')
    model = models.CharField(max_length=30, blank=True, null=True, verbose_name='机台网络')
    status_detail = models.CharField(max_length=30, blank=True, null=True, verbose_name='测试功能')
    fused = models.CharField(max_length=30, blank=True, null=True, verbose_name='测试类型')
    config = models.CharField(max_length=30, blank=True, null=True, verbose_name='配置')
    display = models.CharField(max_length=30, null=True, blank=True, verbose_name="显示器", )
    nand = models.CharField(max_length=30, null=True, blank=True, verbose_name="内存", )
    date_in = models.DateField(null=True, blank=True, verbose_name="入库日期")  # 系統自動录入
    date_out = models.TextField(null=True, blank=True, max_length=60, verbose_name="出库日期")  # 系統自動录入
    units_status = models.CharField(max_length=20, choices=STATE_TYPE, default="1", verbose_name="狀態")  # 系統自動录入
    recuser = models.CharField(max_length=30, null=True, blank=True, verbose_name="入庫者", )  # 系統自動录入

    hw_build_detail = models.CharField(max_length=100, null=True, blank=True, verbose_name="HW Build(Detail)", )
    front_color = models.CharField(max_length=60, null=True, blank=True, verbose_name="Front Color", )
    rear_color = models.CharField(max_length=60, null=True, blank=True, verbose_name="Rear Color", )
    soc = models.CharField(max_length=60, null=True, blank=True, verbose_name="SOC", )
    housing = models.CharField(max_length=60, null=True, blank=True, verbose_name="Housing", )
    tm_grading = models.CharField(max_length=60, null=True, blank=True, verbose_name="TM Grading", )
    grape = models.CharField(max_length=60, null=True, blank=True, verbose_name="Grape", )
    nand_type = models.CharField(max_length=60, null=True, blank=True, verbose_name="NAND Type", )
    die_name = models.CharField(max_length=60, null=True, blank=True, verbose_name="Die Name", )
    battery_detail = models.CharField(max_length=100, null=True, blank=True, verbose_name="Battery Detail", )
    battery_confirm = models.CharField(max_length=60, null=True, blank=True, verbose_name="Battery Confirm", )
    mesa_flex = models.CharField(max_length=100, null=True, blank=True, verbose_name="Mesa Flex", )
    wifi_vender = models.CharField(max_length=60, null=True, blank=True, verbose_name="WiFi Vender", )
    WF1 = models.CharField(max_length=60, null=True, blank=True, verbose_name="WF1", )
    wf2 = models.CharField(max_length=60, null=True, blank=True, verbose_name="WF2", )
    wf3 = models.CharField(max_length=30, null=True, blank=True, verbose_name="WF3", )
    wf5 = models.CharField(max_length=60, null=True, blank=True, verbose_name="WF5", )
    wf5p = models.CharField(max_length=60, null=True, blank=True, verbose_name="WF5P", )
    wf3_metrocirc = models.CharField(max_length=60, null=True, blank=True, verbose_name="WF3 Metrocirc", )
    wf5_metrocirc = models.CharField(max_length=60, null=True, blank=True, verbose_name="WF5 Metrocirc", )
    wf_sw_l = models.CharField(max_length=60, null=True, blank=True, verbose_name="WF_SW_L", )
    wf_sw_r = models.CharField(max_length=60, null=True, blank=True, verbose_name="WF_SW_R", )
    front_camera = models.CharField(max_length=60, null=True, blank=True, verbose_name="Front Camera", )
    rear_camera = models.CharField(max_length=30, null=True, blank=True, verbose_name="Rear Camera", )
    mikey_flex = models.CharField(max_length=60, null=True, blank=True, verbose_name="Mikey flex (Audio J Flex)", )
    fh_spk = models.CharField(max_length=60, null=True, blank=True, verbose_name="FH L/R SPK", )
    chin_spk = models.CharField(max_length=60, null=True, blank=True, verbose_name="Chin L/R SPK", )
    spv_flex = models.CharField(max_length=60, null=True, blank=True, verbose_name="SPV Flex", )
    microphone = models.CharField(max_length=60, null=True, blank=True, verbose_name="Microphone (Mic Flex)", )
    microphone2 = models.CharField(max_length=60, null=True, blank=True, verbose_name="Microphone (Mic2 Flex)", )
    c3_flex = models.CharField(max_length=60, null=True, blank=True, verbose_name="C3 Flex", )
    c4_flex = models.CharField(max_length=60, null=True, blank=True, verbose_name="C4 Flex", )
    mlb = models.CharField(max_length=60, null=True, blank=True, verbose_name="MLB", )
    mlb_soc = models.CharField(max_length=60, null=True, blank=True, verbose_name="MLB Soc", )
    pcb = models.CharField(max_length=60, null=True, blank=True, verbose_name="PCB", )
    bash_flex = models.CharField(max_length=60, null=True, blank=True, verbose_name="Bash Flex", )
    sim_flex = models.CharField(max_length=60, null=True, blank=True, verbose_name="SIM Flex", )
    mimosa = models.CharField(max_length=60, null=True, blank=True, verbose_name="Mimosa", )
    autobahn_flex = models.CharField(max_length=30, null=True, blank=True, verbose_name="Autobahn Flex", )
    edp_flex = models.CharField(max_length=60, null=True, blank=True, verbose_name="EDP Flex", )
    io_bonding = models.CharField(max_length=60, null=True, blank=True, verbose_name="IO Bonding", )
    gyro_type = models.CharField(max_length=60, null=True, blank=True, verbose_name="Gyro Type", )
    appleoscar = models.CharField(max_length=60, null=True, blank=True, verbose_name="AppleOscarAccelerometer(Accel)", )
    dram = models.CharField(max_length=60, null=True, blank=True, verbose_name="DRAM", )
    e75 = models.CharField(max_length=60, null=True, blank=True, verbose_name="E75 TriStar", )
    full_lam = models.CharField(max_length=60, null=True, blank=True, verbose_name="Full Lam", )
    unit_weight = models.CharField(max_length=60, null=True, blank=True, verbose_name="Unit Weight", )
    ecid = models.CharField(max_length=60, null=True, blank=True, verbose_name="16进制 ECID", )
    apecid = models.CharField(max_length=60, null=True, blank=True, verbose_name="10进制 APECID", )
    snum = models.CharField(max_length=60, null=True, blank=True, verbose_name="SNUM", )
    euicccsn = models.CharField(max_length=100, null=True, blank=True, verbose_name="EUICCCSN", )
    unit_no = models.CharField(max_length=60, null=True, blank=True, verbose_name="Unit No.", )
    aapn = models.CharField(max_length=60, null=True, blank=True, verbose_name="AAPN", )
    hhpn = models.CharField(max_length=60, null=True, blank=True, verbose_name="HHPN", )
    wo = models.CharField(max_length=60, null=True, blank=True, verbose_name="WO", )
    allocatedto_group = models.CharField(max_length=50, null=True, blank=True, verbose_name="AllocatedTo/Group", )
    apple_dri = models.CharField(max_length=60, null=True, blank=True, verbose_name="Apple DRI", )
    pt_no = models.CharField(max_length=60, null=True, blank=True, verbose_name="PT No.", )
    apple_po = models.CharField(max_length=60, null=True, blank=True, verbose_name="Apple PO", )
    boxsn = models.CharField(max_length=60, null=True, blank=True, verbose_name="倉碼", )
    certification_period = models.CharField(max_length=60, null=True, blank=True, verbose_name="認證期限", )
    accessory = models.CharField(max_length=60, null=True, blank=True, verbose_name="Accessory", )
    presence_laser = models.CharField(max_length=60, null=True, blank=True, verbose_name="有無鐳射", )
    card = models.CharField(max_length=60, null=True, blank=True, verbose_name="是否带卡", )
    card_type = models.CharField(max_length=60, null=True, blank=True, verbose_name="卡型号", )
    detail_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="Detail Comment", )

    class Meta:
        verbose_name = "IPad庫存表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sn


# 配件详情表
class AccessDetails(models.Model):
    """
     当前设备库存信息表
    """
    STATUS_TYPE = (("1", "In Use"), ("2", "Disuse"), ("3", "Other"))
    accessory = models.CharField(max_length=60, verbose_name="Accessory")
    vender = models.CharField(max_length=60, verbose_name="Vender")
    hw_build = models.CharField(max_length=60, verbose_name="HW Build")
    config = models.CharField(max_length=60, verbose_name="Config")
    # status = models.CharField(max_length=60, verbose_name="Status")
    status = models.CharField(max_length=30, choices=STATUS_TYPE, default="1", verbose_name="狀態")  # 系統自動录入
    qty = models.CharField(max_length=60, verbose_name="QTY")
    box_sn = models.CharField(max_length=60, verbose_name="盒子SN")
    sn = models.CharField(max_length=60, verbose_name="SN")
    contact_address = models.CharField(max_length=60, verbose_name="Contact&Address")
    date_in = models.DateField(null=True, blank=True, verbose_name="Date in")
    date_out = models.TextField(null=True, blank=True, max_length=60, verbose_name="Date out")
    comment = models.TextField(max_length=60, verbose_name="Comment")
    ca_sn = models.CharField(max_length=60, verbose_name="仓码")
    store = models.CharField(max_length=60, verbose_name="储位")
    aapn = models.CharField(max_length=60, verbose_name="AAPN")
    hhpn = models.CharField(max_length=60, verbose_name="HHPN")
    wo = models.CharField(max_length=60, verbose_name="WO")
    recuser = models.CharField(max_length=30, null=True, blank=True, verbose_name="入庫者", )  # 系統自動录入

    class Meta:
        verbose_name = "配件库存信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.accessory
