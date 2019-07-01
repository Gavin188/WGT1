# -*- coding:utf-8 -*-
from django import template
register = template.Library()

# 自定义过滤器:获取绝对值，### 用于解决django中模板语言的求余问题。
@register.filter
def get_mod(arg1, arg2):
    return arg1 % int(arg2)
