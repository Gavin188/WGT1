# @Time   : 2019/10/17 23:13
# @Author : Gavin
# @File   : forms.py

from django import forms

from dqe.models import OperateCacheTable, Project, Stage, Fused, IpadDetails, ApplyListDetail

# # 庫存
# class InventoryCreateForm(forms.ModelForm):
#     class Meta:
#         model = Inventory
#         # fields = '__all__'
#         fields = ['fk_project', 'fk_stage', 'rel', 'sn', 'state', 'remark', 'fk_pt']
#         # exclude = ['自定义属性名',]


# 操作緩存
from system.models import Access


class OperateCacheTableCreateForm(forms.ModelForm):
    class Meta:
        model = OperateCacheTable
        fields = '__all__'


# 操作緩存
class IpadDetailsCreateForm(forms.ModelForm):
    class Meta:
        model = IpadDetails
        fields = '__all__'


#
# # 申请單
# class ApplyCreateForm(forms.ModelForm):
#     class Meta:
#         model = Apply
#         fields = '__all__'


# # 申请详情
# class ApplyDetailCreateForm(forms.ModelForm):
#     class Meta:
#         model = ApplyDetail
#         fields = '__all__'


# 专案表
class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


# 階段表
class StageCreateForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = '__all__'


#
# # 产品类型表
# class ProductTypeCreateForm(forms.ModelForm):
#     class Meta:
#         model = ProductType
#         fields = '__all__'


# 版本类型表
class FusedCreateForm(forms.ModelForm):
    class Meta:
        model = Fused
        fields = ['fname']


# 配件
class AccessCreateForm(forms.ModelForm):
    class Meta:
        model = Access
        fields = ['access']


# # 配件
# class ApplyListDetailForm(forms.ModelForm):
#     class Meta:
#         model = ApplyListDetail
#         # fields = ['platform', 'stage', 'type', 'model', 'timeState', 'qty', 'comments']
#         fields = '__all__'
#         exclude = ['fk_apply', 'lendDate', 'lendUnit', 'machineState']
