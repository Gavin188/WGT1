# -*- coding:utf-8 -*-
from django import template

register = template.Library()


# 自定义过滤器:获取绝对值，### 用于解决django中模板语言的求余问题。
# 自定义过滤器就是接受一个或者连个参数的python函数。例如{{var | foo:"bar"}}，过滤器foo接受变量var和参数bar
@register.filter
def get_mod(arg1, arg2):
    return arg1 % int(arg2)


def dynamicUpdateObjFields(obj=None, fieldName=None, fieldValue=None):
    print(obj, fieldName, fieldValue)
    try:
        if obj and fieldName:
            setattr(obj, fieldName, fieldValue)
            obj.save()
            return '修改成功'
    except Exception as e:
        print(e)
    return '修改失败'
