from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from dps_main.models import Cause, Promise


def _no_id(**kwargs):
    """
    Strip Ids
    """
    _kwargs = {**kwargs}
    if 'id' in _kwargs:
        _kwargs.pop('id')
    return _kwargs


class ActionHelper(object):
    """
    Launches actions that may be executed within the context of a user
    """

    def __init__(self, user: User) -> None:
        """
        :param user:
        :type user: User
        """
        self.user = user

    @staticmethod
    def ping():
        return 'pong'

    def create_cause(self, **kwargs):
        """
        Only admins can create causes
        """
        if self.user.is_superuser:
            return Cause.objects.create(**_no_id(**{**kwargs, **{'creator': self.user}}))
        raise PermissionDenied()

    @classmethod
    def list_causes(cls):
        """
        Everyone gets to see causes, even anonymous users
        :return: QuerySet
        """
        return Cause.objects.all()

    def list_available_causes(self):
        """
        Lists causes where the current user hasn't promised
        :return: QuerySet
        """
        if self.user.is_authenticated:
            return Cause.objects.filter(~Q(id__in=Promise.objects.values_list('cause').filter(user=self.user)))
        return self.list_causes()

    @classmethod
    def get_cause(cls, _id):
        """
        Gets the details of a cause
        """
        return Cause.objects.get(pk=_id)

    def update_cause(self, _id, **kwargs):
        """
        Only admins can update causes
        """
        if self.user.is_superuser:
            Cause.objects.filter(pk=_id).update(**_no_id(**kwargs))
            return
        raise PermissionDenied()

    def delete_cause(self, _id):
        """
        Only admins can delete causes
        """
        if self.user.is_superuser:
            Cause.objects.filter(pk=_id).delete()
            return
        raise PermissionDenied()

    def add_promise_to_cause(self, cause_id, **kwargs):
        """
        Allows a user to make a promise agains a cause
        """
        return Promise.objects.create(**_no_id(**{**kwargs, **{'user': self.user, 'cause_id': cause_id}}))

    def list_promises(self):
        """
        Lists all visible promises.
        Admins see all
        Members see promises they own
        :return:
        """
        q = Promise.objects.all()
        if not self.user.is_superuser:
            q = q.filter(user=self.user)
        return q

    def get_promise(self, _id):
        """
        Gets a promise by id
        :param _id:
        :return:
        """
        q = Promise.objects.filter(pk=_id)
        if not self.user.is_superuser:
            q = q.filter(user=self.user)
        return q.get()

    def update_promise(self, _id, **kwargs):
        """
        Update a promise
        :param _id:
        :param kwargs:
        :return:
        """
        q = Promise.objects.filter(pk=_id)
        if not self.user.is_superuser:
            q = q.filter(user=self.user)
        q.update(**_no_id(**kwargs))

    def delete_promise(self, _id):
        """
        Delete a promise
        :return:
        """
        q = Promise.objects.filter(pk=_id)
        if not self.user.is_superuser:
            q = q.filter(user=self.user)
        q.delete()

    def list_promises_by_cause(self, cause_id):
        """
        Get all promises attached to cause
        :return:
        """
        if self.user.is_superuser:
            return Promise.objects.filter(cause_id=cause_id)
        raise PermissionDenied()

    def get_promise_for_cause(self, cause_id):
        """
        Get own promise attached to cause
        :return:
        """
        if self.user.is_authenticated:
            return Promise.objects.filter(cause_id=cause_id, user=self.user)
        return Promise.objects.none()

    def get_promise_for_cause_(self, cause_id):
        """
        Get own promise attached to cause
        :return:
        """
        if self.user.is_authenticated:
            return Promise.objects.get(cause_id=cause_id, user=self.user)
        return None

    def list_all_causes_promised(self):
        """
        Gets all causes that have been promised
        :return:
        """
        if self.user.is_authenticated:
            return Cause.objects.filter(id__in=Promise.objects.values_list('cause'))
        raise PermissionDenied
