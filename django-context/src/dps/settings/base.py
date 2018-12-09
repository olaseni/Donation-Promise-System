from .default import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# normalizes what Django thinks is the base_dir
BASE_DIR = os.path.dirname(BASE_DIR)

# Application definition

# INSTALLED_APPS
INSTALLED_APPS = ['dps_main.apps.DpsMainConfig'] + INSTALLED_APPS + ['rest_framework']

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

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'dps_main.permissions.rest_framework.SafeDjangoModelPermissions'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}
