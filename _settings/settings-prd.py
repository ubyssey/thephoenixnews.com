import os

from phoenix.secrets import Secrets

from dispatch.default_settings import *

BASE_URL = 'https://thephoenixnews.com/'
CANONICAL_DOMAIN = 'thephoenixnews.com'

SECRET_KEY = Secrets.get('SECRET_KEY')

INSTALLED_APPS += ['phoenix', 'django_user_agents']

ALLOWED_HOSTS = [
    'thephoenixnews.com',
    'www.thephoenixnews.com',
]

ROOT_URLCONF = 'phoenix.urls'

USE_TZ = True

TIME_ZONE = 'America/Vancouver'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '/cloudsql/%s' % Secrets.get('SQL_HOST'),
        'NAME': os.environ['CURRENT_VERSION_ID'].split('.')[0],
        'USER': Secrets.get('SQL_USER'),
        'PASSWORD': Secrets.get('SQL_PASSWORD'),
        'PORT': 3306,
    }
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

SESSION_ENGINE = 'gae_backends.sessions.cached_db'
CACHES = {
    'default': {
        'BACKEND': 'gae_backends.memcache.MemcacheCache',
    }
}

MIDDLEWARE_CLASSES += [
    'canonical_domain.middleware.CanonicalDomainMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

# GCS File Storage
DEFAULT_FILE_STORAGE = 'django_google_storage.storage.GoogleStorage'

GS_ACCESS_KEY_ID = Secrets.get('GS_ACCESS_KEY_ID')
GS_SECRET_ACCESS_KEY = Secrets.get('GS_SECRET_ACCESS_KEY')
GS_STORAGE_BUCKET_NAME = 'phoenix-news'
GS_LOCATION = 'media'
GS_USE_SIGNED_URLS = True

STATICFILES_DIRS += (
    os.path.join(os.path.dirname(__file__), 'static/dist'),
)

STATIC_URL = 'https://phoenix-news.storage.googleapis.com/static/'
MEDIA_URL = 'https://phoenix-news.storage.googleapis.com/media/'

# Use in-memory file handler on Google App Engine
FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.MemoryFileUploadHandler',]
FILE_UPLOAD_MAX_MEMORY_SIZE = 25621440

EMAIL_HOST = Secrets.get('EMAIL_HOST')
EMAIL_PORT = 465
EMAIL_HOST_USER = Secrets.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = Secrets.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
