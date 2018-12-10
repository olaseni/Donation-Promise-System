import logging

from django.conf import settings
from django.db.backends.signals import connection_created
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .utilities.routines import create_default_superuser, create_default_group, assign_default_group_to_user, \
    hydrate_default_group

# Get an instance of a logger
logger = logging.getLogger(__name__)


def initialize():
    """
    Does nothing at the moment
    """
    pass


# noinspection PyBroadException
def swallow_exception(callback, *args, **kwargs):
    """
    Swallow all exceptions that could inhibit the program flow. Log the exception so the application still keeps track
    """
    if callback:
        try:
            # don't run signals during tests
            if settings.ENVIRONMENT == 'test':
                return
            callback(*args, **kwargs)
        except Exception as e:
            logger.error("Exception in #swallow_exception #{1}, {0}".format(e, callback))


@receiver(connection_created, dispatch_uid="db_connection_created")
def on_connection_created(sender, **kwargs):
    """
    Routines that will run when the first DB connection is made
    """
    if sender:
        swallow_exception(create_default_superuser)
        swallow_exception(create_default_group)
        swallow_exception(hydrate_default_group)


@receiver(post_save, sender=get_user_model(), dispatch_uid="post_save_user")
def on_model_saved(sender, instance, created, **kwargs):
    """
    Routines that run when a user was saved
    """
    if created is True:
        swallow_exception(hydrate_default_group)
        swallow_exception(assign_default_group_to_user, user_instance=instance)
