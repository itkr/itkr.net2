from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'cores.wsgi.production.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'simpledjango',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
