# Generated by Django 2.2.2 on 2019-08-09 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overtime', '0011_auto_20190805_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tname', models.CharField(default='54', max_length=30, verbose_name='加班时数')),
                ('tnumber', models.CharField(default='2', max_length=30, verbose_name='周加班次数')),
            ],
            options={
                'verbose_name': '加班提报',
                'verbose_name_plural': '加班提报',
            },
        ),
    ]