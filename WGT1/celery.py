from __future__ import absolute_import, unicode_literals
from celery import Celery
from datetime import timedelta
from django.conf import settings
import os

'''
Celery 用消息通信，通常使用中间人（Broker）在客户端和职程间斡旋。
这个过程从客户端向队列添加消息开始，之后中间人把消息派送给职程。
'''

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WGT1.settings')
app = Celery('wgt1')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

'''
from __future__ import absolute_import
from celery import Celery, platforms
import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UCS.settings')

from django.conf import settings  # noqa

app = Celery('ucs')
platforms.C_FORCE_ROOT = True

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
'''
