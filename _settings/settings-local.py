import os

from dispatch.default_settings import *

BASE_URL = 'http://localhost:8000/'

SECRET_KEY = '&t7b#38ncrab5lmpe#pe#41coa-8ctwuy@tm0!x8*n_r38x_m*'

ALLOWED_HOSTS = ['localhost', '*']

INSTALLED_APPS += ['phoenix']

INTERNAL_IPS = ['127.0.0.1', 'localhost']

ROOT_URLCONF = 'phoenix.urls'

DEBUG = True
USE_TZ = True

TIME_ZONE = 'America/Vancouver'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'phoenix',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
}

TEMPLATES += [
    {
        'NAME': 'ubyssey',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
        ],
    }
]

STATICFILES_DIRS += (
    os.path.join(os.path.dirname(__file__), 'static/dist'),
)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')

FACEBOOK_CLIENT_ID = ''
FACEBOOK_CLIENT_SECRET = ''
