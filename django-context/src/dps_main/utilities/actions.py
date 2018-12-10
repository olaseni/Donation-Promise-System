from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from dps_main.models import Cause, Promise


class ActionHelper(object):
    """
    Launches actions that may be executed within the context of a user
    """

    def __init__(self, user: get_user_model()) -> None:
        """
        :param user:
        :type user: User
        """
        self.user = user

    @staticmethod
    def _no_id(**kwargs):
        _kwargs = {**kwargs}
        if 'id' in _kwargs:
            _kwargs.pop('id')
        return _kwargs

    def create_cause(self, **kwargs):
        """
        Only admins can create causes
        """
        if self.user.is_superuser:
            return Cause.objects.create(self._no_id(**{**kwargs, **{'creator': self.user}}))
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
        return Cause.objects.filter(~Q(id__in=Promise.objects.values_list('id').filter(user=self.user)))

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
            Cause.objects.filter(pk=_id).update(self._no_id(**kwargs))
        raise PermissionDenied()

    def delete_cause(self, _id):
        """
        Only admins can delete causes
        """
        if self.user.is_superuser:
            Cause.objects.filter(pk=_id).delete()
        raise PermissionDenied()

    def add_promise_to_cause(self, cause_id, **kwargs):
        """
        Allows a user to make a promise agains a cause
        """
        return Promise.objects.create(self._no_id(**{**kwargs, **{'user': self.user, 'cause_id': cause_id}}))

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
        q.update(self._no_id(**kwargs))

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
        return Promise.objects.filter(cause_id=cause_id, user=self.user)

    @classmethod
    def get_all_causes_promised(cls):
        """
        Gets all promises that have been promised
        :return:
        """
        return Cause.objects.filter(id__in=Promise.objects.values_list('id'))
