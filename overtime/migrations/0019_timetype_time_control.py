# Generated by Django 2.2.2 on 2019-09-09 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overtime', '0018_auto_20190903_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetype',
            name='time_control',
            field=models.CharField(choices=[('1', '管控'), ('2', '不管控')], default='1', max_length=30, verbose_name='提报加班日期'),
        ),
    ]
