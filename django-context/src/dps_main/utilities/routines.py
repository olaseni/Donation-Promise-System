"""
This module contains functions that perform several routine initialization tasks
"""

import os
import sys
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

from dps_main.apps import DpsMainConfig

__all__ = ['create_default_superuser', 'create_default_group', 'hydrate_default_group', 'assign_default_group_to_user']

_default_group = 'Members'


def contains_static_variables(**kwargs):
    """
    The equivalence of a C-style static variable helper.
    Use as decorator
    """

    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


def create_default_superuser():
    """
    Creates a default superuser when the first connection is made to the DB
    """
    env = os.environ
    user = env.get('DJANGO_SUPER_USER')
    email = env.get('DJANGO_SUPER_EMAIL')
    password = env.get('DJANGO_SUPER_PASSWORD', User.objects.make_random_password(length=45))

    if user and email and password:
        user_class = get_user_model()
        objects = user_class.objects
        try:
            try:
                objects.get(username=user)
            except user_class.DoesNotExist:
                superuser = objects.create_superuser(user, email, password)
                if superuser:
                    print("Superuser created: {0.username}, {0.email}, {1}".format(superuser, password))
                else:
                    raise Exception("Unable to create superuser")
        except Exception as e:
            sys.stderr.write('#create_default_superuser: Error %s\r\n' % e)
    else:
        sys.stderr.write('#create_default_superuser: Unable to obtain parameters to create default superuser\r\n')


def create_default_group():
    """
    Creates a default group
    """
    Group.objects.get_or_create(name=_default_group)


@contains_static_variables(counter=0)
def hydrate_default_group():
    """
    Retrieve interesting permissions and populate the default group
    """
    # bale if we have executed a convenient number of times
    if hydrate_default_group.counter >= 10:
        return

    # add permissions every user should have
    interesting_permissions = Permission.objects.filter(Q(
        name__contains='view'),
        content_type__in=ContentType.objects.filter(Q(model='cause'), app_label=DpsMainConfig.name))

    # assign these to the default group
    group = Group.objects.get(name=_default_group)
    for permission in interesting_permissions:
        group.permissions.add(permission)

    # increment the execution counter
    hydrate_default_group.counter += 1


def assign_default_group_to_user(user_instance):
    """
    Assigns the default group to this user
    """
    group = Group.objects.get(name=_default_group)
    user_instance.groups.add(group)
