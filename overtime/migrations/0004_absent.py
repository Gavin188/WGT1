# Generated by Django 2.2.2 on 2019-08-03 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('overtime', '0003_auto_20190803_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='Absent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_time', models.CharField(blank=True, max_length=30, null=True, verbose_name='申请时间')),
                ('absent_type', models.CharField(choices=[('1', '漏刷卡'), ('2', '办卡中'), ('3', '卡机异常'), ('4', '公务处理'), ('5', '刷卡地点错误')], default='1', max_length=20, verbose_name='异常原因')),
                ('card_type', models.CharField(choices=[('1', '第一段上班卡'), ('2', '第一段下班卡'), ('3', '第二段上班卡'), ('4', '第二段下班卡'), ('5', '补缺上班卡'), ('6', '补缺下班卡')], default='1', max_length=20, verbose_name='打卡类型')),
                ('startTime', models.CharField(blank=True, max_length=30, null=True, verbose_name='异常工作日')),
                ('time_end_period', models.CharField(blank=True, max_length=30, null=True, verbose_name='异常时间段')),
                ('reason', models.CharField(blank=True, max_length=80, null=True, verbose_name='异常原因')),
                ('fk_apply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='overtime.ApplyList', verbose_name='申請單號')),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='用户姓名')),
            ],
            options={
                'verbose_name': '异常申请单',
                'verbose_name_plural': '异常申请单',
            },
        ),
    ]