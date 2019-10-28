from django.test import TestCase


# Create your tests here.

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

#     data = dynamicUpdateObjFields(obj=obj, fieldName=field,
#                                               fieldValue=value)
