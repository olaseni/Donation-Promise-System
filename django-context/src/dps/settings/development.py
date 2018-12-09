# noinspection PyUnresolvedReferences
from .base import *  # noqa: F401

ENVIRONMENT = 'development'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django_python3_": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
