"""
Faker provides a way to create fake/sample model data for internal purposes
"""

import re
from random import randint, choice
from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

from mimesis import Generic

from dps_main.models import Contact, Cause, Promise

_g = Generic('en')
_re_numeric = re.compile("[^\\d.\\-+]")


def _data(model_class, _id=None, create=False, d=None):
    """
    Generic routine for creating demo models
    """
    d = d or dict()
    if _id:
        d['id'] = _id
    model = None
    if create:
        model = model_class.objects.create(**d)
    return d, model


def user(create=False, superuser=False):
    """
    Create a `Sampler/Demo` user
    """
    d = dict(
        username=_g.person.username(),
        email=_g.person.email(),
        password=_g.person.password())
    _user = None
    if create:
        o = User.objects
        m = o.create_superuser if superuser else o.create_user
        _user = m(**d)
    return d, _user


def bulk_users(size):
    """
    Bulk create a bunch of `Sampler/Demo` users of size `size`
    """
    indices = range(size)
    User.objects.bulk_create([User(**user(superuser=choice([True, False]))[0]) for _ in indices])


def contact(_id=None, create=False):
    """
    Create a `Sampler/Demo` contact
    """
    return _data(Contact, _id=_id, create=create, d=dict(
        first_name=_g.person.name(),
        last_name=_g.person.last_name(),
        address=_g.address.address(),
        phone=_g.person.telephone(),
        email=_g.person.email()))


def cause(_id=None, create=False, creator=None, _contact=None):
    """
    Create a `Sampler/Demo` cause
    """
    if not creator or not creator.is_superuser:
        raise PermissionDenied()
    if not _contact:
        _contact = contact(create=create)
        _contact = _contact[1] if create else _contact[0]
    return _data(Cause, _id=_id, create=create, d=dict(
        contact=_contact,
        title=_g.text.title(),
        description=_g.text.text(quantity=randint(6, 20)),
        expiration_date=_g.datetime.datetime(start=date.today().year).date(),
        target_amount=float(_re_numeric.sub('', _g.business.price())),
        illustration=_g.internet.stock_image(500, 500),
        creator=creator
    ))


def bulk_causes(size, creator=None):
    """
    Bulk create a bunch of causes of size `size`.
    A creator is created if none is supplied
    :return the creator
    """
    if not creator:
        _, creator = user(create=True, superuser=True)
    indices = range(size)
    Contact.objects.bulk_create([Contact(**contact()[0]) for _ in indices])
    contacts = Contact.objects.all()
    Cause.objects.bulk_create(
        [Cause(**cause(creator=creator, _contact=contacts[index])[0]) for index in indices])
    return creator


def make_promise(_id=None, create=False, user=None, cause=None, amount=None):
    """
    Create a `Sampler/Demo` promise
    """
    if user and cause:
        try:
            return _data(Promise, _id=_id, create=create, d=dict(
                cause=cause,
                user=user,
                amount=amount or float(_re_numeric.sub('', _g.business.price())),
                target_date=_g.datetime.datetime(start=date.today().year).date()
            ))
        except IntegrityError:
            pass


def make_bulk_promises_with_data_list(promises_list: list):
    """
    Bulk make a bunch of promises in `promises_list`
    """
    Promise.objects.bulk_create([Promise(**promise) for promise in promises_list])


def make_bulk_promises(size, users=None, causes=None):
    """
    Bulk make a bunch of promises of size `size`, using existing/supplied users and causes as seed references
    """
    indices = range(size)
    users = users or User.objects.all()
    causes = causes or Cause.objects.all()
    unique = []
    promises_list = []
    try:
        for _ in indices:
            _user = choice(users)
            _cause = choice(causes)
            _key = (_user.id, _cause.id)
            i = 0 # iteration check
            while _key in unique:
                _user = choice(users)
                _cause = choice(causes)
                _key = (_user.id, _cause.id)
                i = i + 1
                if i > 100:
                    break

            promises_list.append(make_promise(user=_user, cause=_cause)[0])
            unique.append(_key)

        make_bulk_promises_with_data_list(promises_list)
    except IntegrityError as ie:
        return ie
