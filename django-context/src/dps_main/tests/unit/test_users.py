from os import environ
from unittest.mock import patch

from django.contrib.auth.models import User, Group
from dps_main.tests import DpsTestCase


# noinspection PyBroadException
def _swallow_exception(callback, *args, **kwargs):
    """
    Swallow all exceptions...
    """
    if callback:
        try:
            callback(*args, **kwargs)
        except Exception:
            pass


class UserTestCase(DpsTestCase):

    @classmethod
    @patch('dps_main.signals.swallow_exception', _swallow_exception)
    def setUpClass(cls):
        """
        One time setup fixtures, like signals
        """
        from dps_main import signals
        signals.initialize()
        super().setUpClass()

    def setUp(self):
        """
        Sets up a user fixture
        """
        self.assertTestEnvironment()
        User.objects.create_user('potus', 'potus@whitehouse.gov', 'flotus')

    def test_user_created(self):
        """
        GIVEN a django application
        WHEN user creation is stimulated
        THEN a user of the appropriate paramter should exist
        """
        q = User.objects
        self.assertGreaterEqual(q.count(), 1)
        try:
            user = q.get(username='potus')
            self.assertIsInstance(user, User)
            self.assertEqual(user.email, 'potus@whitehouse.gov')
        except User.DoesNotExist:
            self.fail("User 'potus' should exist")

    def test_default_group(self):
        """
        GIVEN a django application
        WHEN application is active
        THEN a default group should be created and exist on application startup
        """
        from dps_main.utilities.routines import get_default_group
        try:
            group = Group.objects.get(name=get_default_group())
            self.assertIsInstance(group, Group)
        except Group.DoesNotExist:
            self.fail("A default group should exist")

    def test_super_user_created(self):
        """
        GIVEN a django application
        WHEN application is started at first
        THEN a super user should be created from environment vars
        """
        django_super_user = environ.get('DJANGO_SUPER_USER', None)
        self.assertIsInstance(django_super_user, str)
        self.assertNotEqual(django_super_user.strip(), '')
        try:
            self.assertIsInstance(User.objects.get(username=django_super_user), User)
        except User.DoesNotExist:
            self.fail(F"Superuser [{django_super_user}] should exist")
