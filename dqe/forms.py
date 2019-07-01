# @Time   : 2018/10/17 23:13
# @Author : RobbieHan
# @File   : forms.py

import re
from django import forms
from django.contrib.auth import get_user_model
from dqe.models import Inventory, ApplyDetail, OperateCacheTable, Apply, Project, Stage, ProductType


#庫存
class InventoryCreateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        #fields = '__all__'
        fields = ['fk_project','fk_stage','rel','sn','state','remark','fk_pt']
        #exclude = ['自定义属性名',]

#操作緩存
class OperateCacheTableCreateForm(forms.ModelForm):
    class Meta:
        model = OperateCacheTable
        fields = '__all__'

#申请單
class ApplyCreateForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = '__all__'

#申请详情
class ApplyDetailCreateForm(forms.ModelForm):
    class Meta:
        model = ApplyDetail
        fields = '__all__'

#专案表
class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

#階段表
class StageCreateForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = '__all__'

#产品类型表
class ProductTypeCreateForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = '__all__'