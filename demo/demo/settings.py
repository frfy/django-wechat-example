# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Django settings for demo project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm+8@0kna^t-#0sb45uv8n^_jz%e9myq(i2=oi)h_dn94$z&e@s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'wechat',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': ['127.0.0.1:6379'],
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': -1,
        },
    },
    # 存放微信公众号 token
    'wechat': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': ['127.0.0.1:6379'],
        'OPTIONS': {
            'DB': 2,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': -1,
        },
    }
}

#==============================================================================
# 微信第三方平台配置
#==============================================================================
COMPONENT_APP_ID = 'app_id'
COMPONENT_APP_SECRET = '0c79eferferfeferf0cc0be99b20a18faeb'
COMPONENT_APP_TOKEN = 'srgewgegerferf'
COMPONENT_ENCODINGAESKEY = 'bz5LSXhcaIBIBKJWZpk2tRl4fiBVbfPN5VlYgwXKTwp'
# 公众号授权链接，大括号中是需要替换的部分
AUTH_URL = (
    "https://mp.weixin.qq.com/cgi-bin/componentloginpage"
    "?component_appid={component_appid}&pre_auth_code="
    "{pre_auth_code}&redirect_uri={redirect_uri}"
)
# 授权成功之后返回链接
AUTH_REDIRECT_URI = 'http://www.somewebsite.com/wechat/authorized'
# 开放平台发布前测试
TEST_APPID = 'wx570bc396a51b8ff8'


#==============================================================================
# Celery配置
#==============================================================================
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
BROKER_URL = "redis://127.0.0.1:6379/10"
CELERY_TASK_RESULT_EXPIRES = 10
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_ENABLE_UTC = False
UTC_ENABLE = False
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'pickle'
CELERYD_MAX_TASKS_PER_CHILD = 2000
CELERY_TIMEZONE = 'UTC'
CELERYD_TASK_LOG_LEVEL = 'INFO'
CELERY_DEFAULT_EXCHANGE = 'default'
# 定时任务配置
CELERYBEAT_SCHEDULE = {
    # 每小时刷新所有公众号 token
    "refresh_all_wechat_token": {
        'task': 'wechat.tasks.refresh_all_wechat_token',
        'schedule': crontab(hour='*', minute=10),
    }
}
