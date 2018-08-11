# Deployment settings

import os

from dispatch.default_settings import *

SECRET_KEY = 'TEMP-KEY'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('SQL_DATABASE_NEW'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'OPTIONS': {
            'unix_socket': os.environ.get('SQL_SOCKET')
        }
    }
}

STATICFILES_DIRS += (
    os.path.join(os.path.dirname(__file__), 'static/dist'),
)

STATIC_ROOT = '/home/travis/build/ubyssey/thephoenixnews.com/gcs/static'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
