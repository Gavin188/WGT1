from django.db import models

# Create your models here.

# 时间安排
import system


class TimeArrange(models.Model):
    pub_date = models.DateField(auto_now_add=False, verbose_name='发布时间')

    class Meta:
        verbose_name = "时间安排"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pub_date


#  任务安排
class TaskArrange(models.Model):
    '''
    state :
         一键申请 判断是否已经申请，
         已经申请，提示状态，防止重复申请
    '''
    NAME_TYPE = (("1", "未申请"), ("2", "已申请"))
    state = models.CharField(max_length=30, choices=NAME_TYPE, default="1", blank=True, null=True,
                             verbose_name="申請状态")
    wgt_no = models.CharField(max_length=30, blank=True, null=True, verbose_name="WGT No.")
    serial_no = models.CharField(max_length=30, blank=True, null=True, verbose_name="Serial No")
    fused = models.CharField(max_length=30, blank=True, null=True, verbose_name="Fused")
    nand = models.CharField(max_length=30, blank=True, null=True, verbose_name="NAND")
    test_build = models.CharField(max_length=30, blank=True, null=True, verbose_name="Test Build")
    tester = models.CharField(max_length=30, blank=True, null=True, verbose_name="Tester")
    comments = models.CharField(max_length=100, blank=True, null=True, verbose_name="Comments")
    upload_user = models.CharField(max_length=30, blank=True, null=True, verbose_name="上传者")
    task_date = models.ForeignKey("TimeArrange", blank=True, null=True, on_delete=models.CASCADE, verbose_name="安排时间")

    class Meta:
        verbose_name = "测试安排"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.wgt_no


#  测试安排
class BugRegister(models.Model):
    date = models.DateField(auto_now_add=False, verbose_name='登记日期')
    group = models.CharField(max_length=30, blank=True, null=True, verbose_name="提报小组")
    find_per = models.CharField(max_length=30, blank=True, null=True, verbose_name="发现人")
    sub_per = models.CharField(max_length=30, blank=True, null=True, verbose_name="提报人")
    radar_id = models.CharField(max_length=30, blank=True, null=True, verbose_name="雷达ID")
    desc = models.CharField(max_length=30, blank=True, null=True, verbose_name="描述")
    comments = models.CharField(max_length=100, blank=True, null=True, verbose_name="备注")

    # fk_TimeArrange = models.ForeignKey("TimeArrange", blank=True, null=True, on_delete=models.CASCADE, verbose_name="安排时间")

    class Meta:
        verbose_name = "测试安排"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


# 案例管理
class CaseRegister(models.Model):
    function = models.CharField(max_length=50, verbose_name='测试项')
    dri = models.CharField(max_length=50, verbose_name='负责人')
    desc = models.CharField(max_length=50, verbose_name='测试说明')

    # desc = models.ForeignKey('system.TestWord', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "案例管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


# class CaseModel(models.Model):
#     '''创建案例管理 - 测试项'''
#     cname = models.CharField(max_length=50, verbose_name='测试项')
#
#     class Meta:
#         verbose_name = "测试项"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.cname


class TestFun(models.Model):
    '''创建案例管理 - 测试项 - 测试模块'''
    case_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='用例编号')
    fk_case = models.ForeignKey('CaseRegister', blank=True, null=True, on_delete=models.CASCADE)
    function = models.CharField(max_length=50, blank=True, null=True, verbose_name='测试模块')
    oper_step = models.CharField(max_length=80, blank=True, null=True, verbose_name='操作步骤')
    expect = models.CharField(max_length=50, verbose_name='期望值')
    # test_results = models.CharField(max_length=50, verbose_name='测试结果')
    # radar_id = models.CharField(max_length=50, verbose_name='雷达ID')
    # comments = models.CharField(max_length=50, verbose_name='comments')
    # fk_time = models.ForeignKey("TimeArrange", blank=True, null=True, on_delete=models.CASCADE, verbose_name="上传时间")
    # fk_test = models.ForeignKey("TestRestful", blank=True, null=True, on_delete=models.CASCADE, verbose_name="测试结果")
    upload_user = models.CharField(max_length=30, blank=True, null=True, verbose_name="上传者")

    class Meta:
        verbose_name = "测试项模块"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_case.function


class TestRestful(models.Model):
    test_results = models.CharField(max_length=50, blank=True, null=True, verbose_name='测试结果')
    radar_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='雷达ID')
    comments = models.CharField(max_length=50, blank=True, null=True, verbose_name='comments')

    # fk_time = models.ForeignKey("TimeArrange", blank=True, null=True, on_delete=models.CASCADE, verbose_name="上传时间")

    fk_test = models.ForeignKey("TestFun", blank=True, null=True, on_delete=models.CASCADE, verbose_name="案例管理")
    create_time = models.DateField(auto_now_add=False, verbose_name='发布时间')

    class Meta:
        verbose_name = "测试结果"

        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fk_test.case_id
