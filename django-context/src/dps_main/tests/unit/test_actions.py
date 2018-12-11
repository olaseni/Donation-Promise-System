from datetime import date

from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied

from dps_main.models import Contact
from dps_main.tests import DpsTestCase
from dps_main.utilities.actions import ActionHelper


class ActionsTestCase(DpsTestCase):

    @staticmethod
    def _create_cause(user, contact, cause_user):
        """
        Shorthand for creating causes
        """
        ah = ActionHelper(user)
        ah.create_cause(title='Title', description='Description', contact=contact,
                        expiration_date=date.today(), target_amount=30000, creator=cause_user)

    def _list_causes(self, user):
        """
        Shorthand for reading causes
        """
        ah = ActionHelper(user)
        return ah.list_causes()

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
        self._create_cause(su, cn, su)

    def test_create_cause_anonymous(self):
        """
        GIVEN an anonymous user
        WHEN attempting to create and read a cause
        THEN creating should fail, while read should work out
        """
        contact = Contact.objects.get(pk=1)
        au = AnonymousUser()
        with self.assertRaises(PermissionDenied):
            self._create_cause(au, contact, au)

        # attempt to read su's cause
        self.assertEqual(len(self._list_causes(au)), 1)

    def test_create_cause_member(self):
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

    def test_create_cause_super(self):
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
