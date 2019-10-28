# 階段表
from django import forms

from overtime.models import Abnormal, Absent, TimeType


# 请假
class AbnormalCreateForm(forms.ModelForm):
    class Meta:
        model = Abnormal
        fields = '__all__'
        exclude = ['username']


# 异常
class AbsentCreateForm(forms.ModelForm):
    class Meta:
        model = Absent
        fields = '__all__'
        exclude = ['username']


# 加班管控
# 公告表
class TimeTypeCreateForm(forms.ModelForm):
    class Meta:
        model = TimeType
        fields = '__all__'
