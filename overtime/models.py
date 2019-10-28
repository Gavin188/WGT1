from django.db import models


# Create your models here.


# 申请单
class ApplyList(models.Model):
    APPLYSTATE_TYPE = (("1", "待簽核"), ("2", "已簽核"), ("3", "已取消"), ("4", "已拒绝"), ("5", "已修改"))
    NAME_TYPE = (("1", "请假"), ("2", "异常"), ("3", "加班"))
    applyNum = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請單號", )
    applyUser = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請人", )
    applyUnit = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請單位", )
    applyType = models.CharField(max_length=30, choices=NAME_TYPE, blank=True, null=True, verbose_name="申請类别", )
    applyDate = models.DateTimeField(auto_now_add=False, verbose_name='申請時間', )
    applyState = models.CharField(max_length=30, choices=APPLYSTATE_TYPE, default="1", blank=True,
                                  verbose_name="申請狀態", )
    confirmTime = models.CharField(max_length=30, blank=True, null=True, verbose_name="确认时间", )

    confirmUser = models.CharField(max_length=30, null=True, blank=True, verbose_name="确认主管")
    confirmDepartment = models.CharField(max_length=30, blank=True, null=True, default='Leader', verbose_name="确认單位", )

    fk_month = models.ForeignKey('AddMonth', blank=True, null=True, on_delete=models.CASCADE, verbose_name="加班月份")

    class Meta:
        verbose_name = "申請單"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.applyNum


#  加班总览- 创建每个月份的字段，由申请单自动生成 显示每一个月的加班情况
class AddMonth(models.Model):
    month = models.CharField(max_length=30, blank=True, null=True, verbose_name="加班月份")

    class Meta:
        verbose_name = "加班月份"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.month


# 请假申请单
class Abnormal(models.Model):
    LEAVE_TYPE = (
        ('1', '事假'), ('2', '路程假'), ('3', '專案事假'), ('4', '年休假'), ('5', '產假'), ('6', '返鄉福利假'), ('7', '婚假'), ('8', '病假'),
        ('9', '喪假'), ('10', '三八婦女節假'))
    # applyNum = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請單號", )
    fk_apply = models.ForeignKey(ApplyList, blank=True, null=True, on_delete=models.CASCADE, verbose_name="申請單號")
    username = models.ForeignKey("system.UserProfile", null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name="用户姓名")
    apply_time = models.CharField(max_length=30, null=True, blank=True, verbose_name="申请时间")
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE, default="1", verbose_name="是否长借")
    startTime = models.CharField(max_length=30, null=True, blank=True, verbose_name="开始工作日")
    endTime = models.CharField(max_length=30, null=True, blank=True, verbose_name="结束工作日")
    leave_start_time = models.CharField(max_length=30, null=True, blank=True, verbose_name="请假开始时间")
    leave_end_time = models.CharField(max_length=30, null=True, blank=True, verbose_name="请假结束时间")
    lengh_time = models.CharField(max_length=30, null=True, blank=True, verbose_name="请假时长")
    time_start_period = models.CharField(max_length=30, null=True, blank=True, verbose_name="请假开始时间段")
    time_end_period = models.CharField(max_length=30, null=True, blank=True, verbose_name="请假结束时间段")
    reason = models.CharField(max_length=80, null=True, blank=True, verbose_name="请假原因")
    agent_name = models.CharField(max_length=80, null=True, blank=True, verbose_name="代理人姓名")
    agent_worknum = models.CharField(max_length=80, null=True, blank=True, verbose_name="代理人工号")

    class Meta:
        verbose_name = "请假申请单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_apply.applyNum


class Absent(models.Model):
    LEAVE_TYPE = (('1', '漏刷卡'), ('2', '办卡中'), ('3', '卡机异常'), ('4', '公务处理'), ('5', '刷卡地点错误'))
    CARD_TYPE = (('1', '第一段上班卡'), ('2', '第一段下班卡'), ('3', '第二段上班卡'), ('4', '第二段下班卡'), ('5', '补缺上班卡'), ('6', '补缺下班卡'))
    # applyNum = models.CharField(max_length=30, blank=True, null=True, verbose_name="申請單號", )
    fk_apply = models.ForeignKey(ApplyList, blank=True, null=True, on_delete=models.CASCADE, verbose_name="申請單號")
    username = models.ForeignKey("system.UserProfile", null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name="用户姓名")
    apply_time = models.CharField(max_length=30, null=True, blank=True, verbose_name="申请时间")
    absent_type = models.CharField(max_length=20, choices=LEAVE_TYPE, default="1", verbose_name="异常原因")
    card_type = models.CharField(max_length=20, choices=CARD_TYPE, default="1", verbose_name="打卡类型")
    startTime = models.CharField(max_length=30, null=True, blank=True, verbose_name="异常工作日")
    time_end_period = models.CharField(max_length=30, null=True, blank=True, verbose_name="异常时间段")
    reason = models.CharField(max_length=80, null=True, blank=True, verbose_name="异常原因")

    class Meta:
        verbose_name = "异常申请单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_apply.applyNum


class AddTime(models.Model):
    fk_apply = models.ForeignKey(ApplyList, blank=True, null=True, on_delete=models.CASCADE, verbose_name="申請單號")
    username = models.ForeignKey("system.UserProfile", null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name="用户姓名")
    data_time = models.CharField(max_length=30, null=True, blank=True, verbose_name="加班时间")
    data_hour = models.CharField(max_length=30, null=True, blank=True, verbose_name="加班小时")
    data_type = models.CharField(max_length=30, null=True, blank=True, verbose_name="加班类型")
    add_content = models.CharField(max_length=100, null=True, blank=True, verbose_name="加班内容")

    class Meta:
        verbose_name = "加班申请单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_apply.applyNum


# 加班小时提报管控
class TimeType(models.Model):
    TIME_TYPE = (('1', '管控'), ('2', '不管控'))
    tname = models.CharField(max_length=30, default='54', verbose_name='加班时数')
    tnumber = models.CharField(max_length=30, default='2', verbose_name='周加班次数')
    tscale = models.CharField(max_length=30, default='0.3', verbose_name='周加班比例')
    tdate = models.CharField(max_length=30, default='25', verbose_name='提报加班日期')
    time_control = models.CharField(max_length=30, default='1', choices=TIME_TYPE, verbose_name='提报加班日期')

    class Meta:
        verbose_name = '加班提报'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tname
