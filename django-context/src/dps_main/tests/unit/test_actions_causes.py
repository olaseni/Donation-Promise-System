from datetime import date

from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied

from dps_main.models import Contact, Cause
from dps_main.tests import DpsTestCase
from dps_main.utilities.actions import ActionHelper


class CauseActionsTestCase(DpsTestCase):

    @staticmethod
    def _create_cause(user, contact, cause_user):
        """
        Shorthand for creating causes
        """
        ah = ActionHelper(user)
        return ah.create_cause(title='Title', description='Description', contact=contact,
                               expiration_date=date.today(), target_amount=30000, creator=cause_user)

    @staticmethod
    def _list_causes(user):
        """
        Shorthand for reading causes
        """
        ah = ActionHelper(user)
        return ah.list_causes()

    @staticmethod
    def _read_cause(user, cause_id):
        """
        Shorthand for reading a cause
        """
        ah = ActionHelper(user)
        return ah.get_cause(cause_id)

    @staticmethod
    def _update_cause(user, cause_id, **kwargs):
        """
        Shorthand for updating a cause
        """
        ah = ActionHelper(user)
        return ah.update_cause(cause_id, **kwargs)

    @staticmethod
    def _delete_cause(user, cause_id):
        """
        Shorthand for deleting a cause
        """
        ah = ActionHelper(user)
        return ah.delete_cause(cause_id)

    def setUp(self):
        """
        Fixtures
        """
        Contact.objects.create(id=1, first_name='First', last_name='Last', address='Address', phone='+00000000',
                               email='a@email.com')
        cn = Contact.objects.create(id=2, first_name='First 2', last_name='Last 2', address='Address',
                                    phone='+00000000',
                                    email='a@email.com')
        User.objects.create_user('user', 'email@email.com', 'fasfj20r92f3')
        su = User.objects.create_superuser('admin5', 'super@email.com', 'sgsgsgsgwt2r2t23')
        # create a cause for a superuser
        cu = self._create_cause(su, cn, su)
        # save ref
        self.cu_id = cu.id

    def test_cause_anonymous(self):
        """
        GIVEN an anonymous user
        WHEN attempting to create and read a cause
        THEN creating/deleting should fail, while read should work out
        """
        contact = Contact.objects.get(pk=1)
        au = AnonymousUser()
        with self.assertRaises(PermissionDenied):
            self._create_cause(au, contact, au)

        # attempt to read su's cause
        self.assertEqual(len(self._list_causes(au)), 1)
        self.assertIsInstance(self._read_cause(au, self.cu_id), Cause)

        # attempt to update su's cause
        with self.assertRaises(PermissionDenied):
            self._update_cause(au, self.cu_id, title='')

        # attempt to delete su's cause
        with self.assertRaises(PermissionDenied):
            self._delete_cause(au, self.cu_id)

    def test_cause_member(self):
        """
        GIVEN a normal member user
        WHEN attempting to create and read a cause
        THEN creating should fail, while read should work out
        """
        contact = Contact.objects.get(pk=1)
        au = User.objects.get(username='user')
        with self.assertRaises(PermissionDenied):
            self._create_cause(au, contact, au)

        # attempt to read su's cause
        self.assertEqual(len(self._list_causes(au)), 1)
        self.assertIsInstance(self._read_cause(au, self.cu_id), Cause)

        # attempt to update su's cause
        with self.assertRaises(PermissionDenied):
            self._update_cause(au, self.cu_id, title='')

        # attempt to delete su's cause
        with self.assertRaises(PermissionDenied):
            self._delete_cause(au, self.cu_id)

    def test_cause_super(self):
        """
        GIVEN a super user
        WHEN attempting to create and read a cause
        THEN creation and reading should work out
        """
        contact = Contact.objects.get(pk=1)
        au = User.objects.get(username='admin5')
        try:
            self._create_cause(au, contact, au)
        except PermissionDenied:
            self.fail('Cause creation should pass')

        # attempt to read su's cause
        self.assertEqual(len(self._list_causes(au)), 2)
        self.assertIsInstance(self._read_cause(au, self.cu_id), Cause)

        # attempt at updating
        try:
            self._update_cause(au, self.cu_id, title='')
            self.assertEqual(self._read_cause(au, self.cu_id).title, '')
        except PermissionDenied:
            self.fail('Cause updates should pass')

        # attempt at deletion
        try:
            self._delete_cause(au, self.cu_id)
            # There should be 1 left
            self.assertEqual(len(self._list_causes(au)), 1)
        except PermissionDenied:
            self.fail('Cause deletion should pass')
