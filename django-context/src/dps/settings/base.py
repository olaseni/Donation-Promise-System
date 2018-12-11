from .default import *

ENVIRONMENT = 'base'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# normalizes what Django thinks is the base_dir
BASE_DIR = os.path.dirname(BASE_DIR)

# Application definition

# INSTALLED_APPS
INSTALLED_APPS = ['dps_main.apps.DpsMainConfig'] + INSTALLED_APPS + ['rest_framework', 'adminplus', 'cacheops']
# Admin plus
INSTALLED_APPS = ['django.contrib.admin.apps.SimpleAdminConfig' if app == 'django.contrib.admin' else app for app in
                  INSTALLED_APPS]

# TEMPLATES

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db',
        'USER': 'db',
        'PASSWORD': 'db',
        'HOST': 'db'
    }
}

# Add a middleware class
MIDDLEWARE += ['dps_main.utilities.middleware.DPSActionsMiddleWare']

# A custom context processor
TEMPLATES[0]['OPTIONS']['context_processors'] += ['dps_main.utilities.processors.get_factotum']

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Django Rest Framework, DRF
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'dps_main.permissions.rest_framework.SafeDjangoModelPermissions'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}

# Redis
# https://redis.io/
REDIS_SERVER = {
    'host': 'redis',
    'port': 6379,
    'db': 1,
}

# Caches
# http://niwinz.github.io/django-redis/latest/
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": F"redis://{REDIS_SERVER.get('host')}:{REDIS_SERVER.get('port')}/{REDIS_SERVER.get('db')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "redis-cache"
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# cacheops
CACHEOPS_REDIS = {**REDIS_SERVER}
CACHEOPS_PREFIX = 'dps_main.utilities.cacheops.cacheops_prefix'
CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60
}
CACHEOPS = {
    'auth.user': {'ops': 'get', 'timeout': 60 * 15},
    'auth.*': {'ops': ('fetch', 'get')},
    'auth.permission': {'ops': 'all'},
    'dps_main.*': {'ops': 'all'},
}
