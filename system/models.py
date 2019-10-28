import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="菜单名")  # unique=True, 这个字段在表中必须有唯一值.
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父菜单")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name="编码")
    url = models.CharField(max_length=128, unique=True, null=True, blank=True)
    number = models.FloatField(null=True, blank=True, verbose_name="编号")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['number']

    @classmethod
    def get_menu_by_request_url(cls, url):
        try:
            return dict(menu=Menu.objects.get(url=url))
        except:
            None


class Role(models.Model):
    """
    角色：用于权限绑定
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="角色")
    permissions = models.ManyToManyField("menu", blank=True, verbose_name="URL授权")
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")


class Structure(models.Model):
    """
    组织架构
    """
    type_choices = (("unit", "部门"), ("department", "小组"))
    name = models.CharField(max_length=60, verbose_name="名称")
    type = models.CharField(max_length=20, choices=type_choices, default="department", verbose_name="类型")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父类架构")

    # resetTime = models.CharField(max_length=20, blank=True, null=True, verbose_name="Reset时长")
    # sendUserEmail = models.TextField(blank=True, null=True, verbose_name="部门邮件组")

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 用户表
class UserProfile(AbstractUser):
    time_choices = (("1", "管控"), ("2", "不管控"))
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")), default="male",
                              verbose_name="性别")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.jpg", max_length=100, null=True,
                              blank=True)
    department = models.ForeignKey("Structure", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="小组")
    post = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    superior = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级主管")
    roles = models.ManyToManyField("role", verbose_name="角色", blank=True)
    worknum = models.CharField(max_length=20, verbose_name="工號")
    level = models.CharField(max_length=20, verbose_name="分类")
    enjoy_company = models.DateField(null=True, blank=True, verbose_name="进集团日期")
    enjoy_wgt = models.DateField(null=True, blank=True, verbose_name="进WGT日期")
    time_control = models.CharField(max_length=30, choices=time_choices, default="1", verbose_name="加班管控")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


# 公告表
class Notice(models.Model):
    tag = models.CharField(max_length=30, blank=True, null=True, verbose_name="标签", )
    relDate = models.DateTimeField(auto_now_add=True, verbose_name='发布日期', )
    relContent = models.TextField(max_length=500, blank=True, null=True, verbose_name="发布内容", )
    relUser = models.CharField(max_length=30, blank=True, null=True, verbose_name="发布者", )
    other = models.CharField(max_length=60, blank=True, null=True, verbose_name="其他", )

    class Meta:
        verbose_name = "公告表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


# Accessory
class Access(models.Model):
    access = models.CharField(max_length=60, blank=True, null=True, verbose_name="配件平台", )

    class Meta:
        verbose_name = "配件信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.access


#  测试管理的 word 文档 -- 采用 CKEditor 第三方插件
class TestWord(models.Model):
    '''这是word 测试说明书'''
    title = models.CharField(max_length=50, verbose_name='标题')
    comments = models.CharField(max_length=30, verbose_name='备注')
    publisher = models.CharField(max_length=30, verbose_name='发布者')
    publish_date = models.DateTimeField(auto_now_add=False, verbose_name='发布时间', default=timezone.now)
    desc_pack = RichTextUploadingField(default='', verbose_name='测试说明内容')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '测试说明书'
        # db_table = verbose_name
        verbose_name_plural = verbose_name
