"""
Django settings for project_price_management project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# 项目的所在的路径
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '82e$3(8l)1mwri=)(@n+y=918jnav6r76pb4kh=1&kti@+ub02'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'DjangoUeditor',
    'dqe',
    'overtime',
    'system',
    'testManage',
    # 'django_adminlte',
    # 'django_adminlte_theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'system.middleware.MenuCollection',
    # 'system.middleware.RbacMiddleware',
]

ROOT_URLCONF = 'WGT1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 内置static -->无需在 html 加载 {%load static%}
            # 'builtins':['django.templatetags.static']
            'libraries': {
                'get_mode': 'dqe.get_mode',
            }
        },
    },
]

# WSGI_APPLICATION = 'WGT1.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 配置使用mysql
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库产品
        'NAME': 'wgt1',  # 数据库名
        'HOST': 'localhost',  # 主机地址，本机使用localhost，生产环境为实际主机ip
        'PORT': '3306',  # 端口
        'USER': 'root',  # 用户名
        'PASSWORD': 'guo123456.',  # 密码
    }

}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'quotation_track_db',
#         'USER': 'root',
#         'PASSWORD': 'yannide123.',
#         'HOST': "127.0.0.1",
#         'PORT': '3306',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


# 媒体
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# 自定以用户模型
AUTH_USER_MODEL = 'system.UserProfile'

LOGIN_URL = '/login/'

# REDIS_SERVER = '10.141.165.225'

# safe url
SAFE_URL = [r'^/$',
            '/login/',
            '/logout',
            '/index/',
            '/media/',
            '/admin/',
            '/ckeditor/',
            ]
# 定时设置
""" 
redis方式
# 定時設置
import djcelery

#当djcelery.setup_loader()运行时，Celery便会去查看INSTALLD_APPS下包含的所有app目录中的tasks.py文件，找到标记为task的方法，将它们注册为celery task。
djcelery.setup_loader()

BROKER_URL = 'redis://127.0.0.1:6379/2'  #设置broker为代理人

CELERY_IMPORTS = ('dqe.tasks')     #导入目标任务文件

CELERY_TIMEZONE = 'Asia/Shanghai'  #设置时区

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'    # 使用了django-celery默认的数据库调度模型,任务执行周期都被存在默认指定的orm数据库中

from datetime import timedelta

CELERYBEAT_SCHEDULE = {

    u'定時任務': {
        "task": "dqe.tasks.interval_task",
        "schedule": timedelta(seconds=5),
        "args": (),
    },

}
"""

""" django作为broker """

# # 定時設置
# BROKER_URL = 'django://localhost:8000//'

# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# CELERY_TIMEZONE = 'Asia/Shanghai'

# CELERYD_MAX_TASKS_PER_CHILD = 10

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# CKEDITOR_UPLOAD_PATH = "upload/"  # 上传图片保存路径，如果没有图片存储或者使用自定义存储位置，那么则直接写  ' ' ,如果是使用django本身的存储方式，那么你就指名一个目录用来存储即可。

# CKEDITOR_UPLOAD_PATH = "uploads/"
# CKEDITOR_IMAGE_BACKEND = 'pillow'

# # 富文本编辑器ckeditor配置
# CKEDITOR_CONFIGS = {
#     'default': {
#         'update': ['Image', 'Update', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
#         'skin': 'moono',
#         'toolbar_Basic': [
#             ['Source', '-', 'Bold', 'Italic']
#         ],
#         'toolbar_YourCustomToolbarConfig': [
#             {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
#             {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
#             {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
#             {'name': 'forms',
#              'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
#                        'HiddenField']},
#             '/',
#             {'name': 'basicstyles',
#              'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
#             {'name': 'paragraph',
#              'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
#                        'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
#                        'Language']},
#             {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
#             {'name': 'insert',
#              'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
#             {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
#             {'name': 'colors', 'items': ['TextColor', 'BGColor']},
#             {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
#             {'name': 'yourcustomtools', 'items': [
#                 # 自定义控件
#                 'Preview',
#                 'Maximize',
#             ]},
#         ],
#         'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
#         'tabSpaces': 4,
#         'extraPlugins': ','.join(
#             [
#                 # your extra plugins here
#                 'div',
#                 'autolink',
#                 'autoembed',
#                 'embedsemantic',
#                 'autogrow',
#                 # 'devtools',
#                 'widget',
#                 'lineutils',
#                 'clipboard',
#                 'dialog',
#                 'dialogui',
#                 'elementspath'
#             ]),
#     }
# }
