from django.db import models


# 专案表
class Project(models.Model):
    pname = models.CharField(max_length=30, verbose_name="專案名稱")

    class Meta:
        verbose_name = "專案表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pname


# 阶段表
class Stage(models.Model):
    fk_project = models.ForeignKey('Project', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="專案名稱")
    sname = models.CharField(max_length=30, verbose_name="階段名稱")

    class Meta:
        verbose_name = "階段表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sname


# 阶段表
class ProductType(models.Model):
    ptname = models.CharField(max_length=30, verbose_name="产品类别名")

    class Meta:
        verbose_name = "产品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ptname


# 庫存表
class Inventory(models.Model):
    STATE_TYPE = (("1", "入庫"), ("2", "已借出"), ("3", "被申請"), ("4", "出库"), ("5", "损坏"))
    fk_project = models.ForeignKey('Project', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="專案名稱")
    fk_stage = models.ForeignKey('Stage', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="階段名稱")
    rel = models.CharField(max_length=30, null=True, blank=True, verbose_name="Rel编号", )  # default="",
    sn = models.CharField(max_length=30, null=True, blank=True, verbose_name="SN", )
    indate = models.DateTimeField(auto_now_add=True, verbose_name='入庫日期', )  # 系統自動录入
    fk_structure = models.ForeignKey('system.Structure', null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name="當前使用部門")
    recuser = models.CharField(max_length=30, null=True, blank=True, verbose_name="入庫者", )  # 系統自動录入
    state = models.CharField(max_length=20, choices=STATE_TYPE, default="1", verbose_name="狀態")
    stayTime = models.CharField(max_length=30, null=True, blank=True, verbose_name="當前部門停留時間", )
    remark = models.TextField(blank=True, null=True, verbose_name="入庫說明")
    currRecUser = models.CharField(max_length=30, null=True, blank=True, verbose_name="當前申請人", )
    currRecDate = models.CharField(max_length=30, null=True, blank=True, verbose_name="當前入庫日期", )
    fk_pt = models.ForeignKey('dqe.ProductType', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="產品類型")
    resetFlag = models.BooleanField(default=False, null=True, blank=True, verbose_name="点击Reset标记")

    class Meta:
        verbose_name = "庫存表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.rel


# Reset记录表
class ResetHistory(models.Model):
    fk_inv = models.ForeignKey('Inventory', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Reset機台")
    resetUser = models.CharField(max_length=36, null=True, blank=True, verbose_name="Reset操作者", )
    resetDept = models.CharField(max_length=36, null=True, blank=True, verbose_name="Reset部门", )
    resetTime = models.DateTimeField(auto_now_add=True, verbose_name='Reset时间', )
    resetRemark = models.CharField(max_length=60, null=True, blank=True, verbose_name="Reset备注", )

    class Meta:
        verbose_name = "Reset记录表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.resetRemark


# 操作緩存表
class OperateCacheTable(models.Model):
    fk_inventory = models.ForeignKey('Inventory', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="申請機台")
    fk_structure = models.ForeignKey('system.Structure', null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name="申請部門")
    opeuser = models.CharField(max_length=30, null=True, blank=True, verbose_name="操作者", )

    class Meta:
        verbose_name = "操作緩存表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_structure.name + "/" + self.fk_inventory.rel


# 申请单
class Apply(models.Model):
    APPLYSTATE_TYPE = (("1", "待簽核"), ("2", "已簽核"),)

    applyNum = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請單號", )

    applyUser = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請人", )
    applyUnit = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請單位", )
    applyDate = models.DateTimeField(auto_now_add=True, verbose_name='申請時間', )
    applyTime = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請時長", )
    applyState = models.CharField(max_length=30, choices=APPLYSTATE_TYPE, default="1", blank=True,
                                  verbose_name="申請狀態", )
    lendRemark = models.CharField(max_length=30, blank=True, null=True, verbose_name="借出單備註", )

    class Meta:
        verbose_name = "申請單"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.applyNum


# 申请单详情表 -- 与库存关联

class ApplyDetail(models.Model):
    MACHINE_STATE = (("1", "未確認"), ("2", "確認"), ("3", "拒絕"),)
    fk_apply = models.ForeignKey(Apply, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="申請單號")
    fk_inventory = models.ForeignKey(Inventory, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="申請機台")
    machineState = models.CharField(max_length=30, choices=MACHINE_STATE, default="1", blank=True,
                                    verbose_name="機台確認狀態", )
    confirmUser = models.CharField(max_length=30, blank=True, null=True, verbose_name="確認人", )
    lendDate = models.DateTimeField(auto_now_add=True, verbose_name='借出時間', )
    lendUnit = models.CharField(max_length=30, blank=True, null=True, verbose_name="借出單位", )
    lendtime = models.CharField(max_length=30, blank=True, null=True, verbose_name="借出時長", )
    remark = models.TextField(blank=True, null=True, verbose_name="機台備註")
    macAppState = models.CharField(max_length=30, blank=True, null=True, verbose_name="機台申請前狀態", )

    class Meta:
        verbose_name = "申請單详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_apply.applyNum


# 机台在该部门下累计使用时长
class RecordTable(models.Model):
    fk_inventory = models.ForeignKey('Inventory', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="申請機台")
    fk_structure = models.ForeignKey('system.Structure', null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name="申請部門")
    stayTimeTotal = models.CharField(max_length=30, blank=True, null=True, verbose_name="累計停留時間", )

    class Meta:
        verbose_name = "記錄表"  # 記錄機台在某部門下的總使用時間
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.stayTimeTotal
