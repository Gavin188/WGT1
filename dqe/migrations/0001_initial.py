# Generated by Django 2.2.2 on 2019-06-20 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applyNum', models.CharField(blank=True, max_length=30, null=True, verbose_name='申請單號')),
                ('applyUser', models.CharField(blank=True, max_length=30, null=True, verbose_name='申請人')),
                ('applyUnit', models.CharField(blank=True, max_length=30, null=True, verbose_name='申請單位')),
                ('applyDate', models.DateTimeField(auto_now_add=True, verbose_name='申請時間')),
                ('applyTime', models.CharField(blank=True, max_length=30, null=True, verbose_name='申請時長')),
                ('applyState', models.CharField(blank=True, choices=[('1', '待簽核'), ('2', '已簽核')], default='1', max_length=30, verbose_name='申請狀態')),
                ('lendRemark', models.CharField(blank=True, max_length=30, null=True, verbose_name='借出單備註')),
            ],
            options={
                'verbose_name': '申請單',
                'verbose_name_plural': '申請單',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rel', models.CharField(blank=True, max_length=30, null=True, verbose_name='Rel编号')),
                ('sn', models.CharField(blank=True, max_length=30, null=True, verbose_name='SN')),
                ('indate', models.DateTimeField(auto_now_add=True, verbose_name='入庫日期')),
                ('recuser', models.CharField(blank=True, max_length=30, null=True, verbose_name='入庫者')),
                ('state', models.CharField(choices=[('1', '入庫'), ('2', '可申請'), ('3', '被申請'), ('4', '出库')], default='1', max_length=20, verbose_name='狀態')),
                ('stayTime', models.CharField(blank=True, max_length=30, null=True, verbose_name='當前部門停留時間')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='入庫說明')),
                ('currRecUser', models.CharField(blank=True, max_length=30, null=True, verbose_name='當前申請人')),
                ('currRecDate', models.CharField(blank=True, max_length=30, null=True, verbose_name='當前入庫日期')),
                ('resetFlag', models.BooleanField(blank=True, default=False, null=True, verbose_name='点击Reset标记')),
            ],
            options={
                'verbose_name': '庫存表',
                'verbose_name_plural': '庫存表',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ptname', models.CharField(max_length=30, verbose_name='产品类别名')),
            ],
            options={
                'verbose_name': '产品类别',
                'verbose_name_plural': '产品类别',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=30, verbose_name='專案名稱')),
            ],
            options={
                'verbose_name': '專案表',
                'verbose_name_plural': '專案表',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(max_length=30, verbose_name='階段名稱')),
                ('fk_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dqe.Project', verbose_name='專案名稱')),
            ],
            options={
                'verbose_name': '階段表',
                'verbose_name_plural': '階段表',
            },
        ),
        migrations.CreateModel(
            name='ResetHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resetUser', models.CharField(blank=True, max_length=36, null=True, verbose_name='Reset操作者')),
                ('resetDept', models.CharField(blank=True, max_length=36, null=True, verbose_name='Reset部门')),
                ('resetTime', models.DateTimeField(auto_now_add=True, verbose_name='Reset时间')),
                ('resetRemark', models.CharField(blank=True, max_length=60, null=True, verbose_name='Reset备注')),
                ('fk_inv', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dqe.Inventory', verbose_name='Reset機台')),
            ],
            options={
                'verbose_name': 'Reset记录表',
                'verbose_name_plural': 'Reset记录表',
            },
        ),
        migrations.CreateModel(
            name='RecordTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stayTimeTotal', models.CharField(blank=True, max_length=30, null=True, verbose_name='累計停留時間')),
                ('fk_inventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dqe.Inventory', verbose_name='申請機台')),
                ('fk_structure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.Structure', verbose_name='申請部門')),
            ],
            options={
                'verbose_name': '記錄表',
                'verbose_name_plural': '記錄表',
            },
        ),
        migrations.CreateModel(
            name='OperateCacheTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opeuser', models.CharField(blank=True, max_length=30, null=True, verbose_name='操作者')),
                ('fk_inventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dqe.Inventory', verbose_name='申請機台')),
                ('fk_structure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.Structure', verbose_name='申請部門')),
            ],
            options={
                'verbose_name': '操作緩存表',
                'verbose_name_plural': '操作緩存表',
            },
        ),
        migrations.AddField(
            model_name='inventory',
            name='fk_project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dqe.Project', verbose_name='專案名稱'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='fk_pt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dqe.ProductType', verbose_name='產品類型'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='fk_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dqe.Stage', verbose_name='階段名稱'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='fk_structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.Structure', verbose_name='當前使用部門'),
        ),
        migrations.CreateModel(
            name='ApplyDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machineState', models.CharField(blank=True, choices=[('1', '未確認'), ('2', '確認'), ('3', '拒絕')], default='1', max_length=30, verbose_name='機台確認狀態')),
                ('confirmUser', models.CharField(blank=True, max_length=30, null=True, verbose_name='確認人')),
                ('lendDate', models.DateTimeField(auto_now_add=True, verbose_name='借出時間')),
                ('lendUnit', models.CharField(blank=True, max_length=30, null=True, verbose_name='借出單位')),
                ('lendtime', models.CharField(blank=True, max_length=30, null=True, verbose_name='借出時長')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='機台備註')),
                ('macAppState', models.CharField(blank=True, max_length=30, null=True, verbose_name='機台申請前狀態')),
                ('fk_apply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dqe.Apply', verbose_name='申請單號')),
                ('fk_inventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dqe.Inventory', verbose_name='申請機台')),
            ],
            options={
                'verbose_name': '申請單详情',
                'verbose_name_plural': '申請單详情',
            },
        ),
    ]