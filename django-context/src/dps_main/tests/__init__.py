from django.conf import settings
from django.test import TestCase


class DpsTestCase(TestCase):

    @classmethod
    def get_settings(cls):
        """
        Returns Django settings in the context of the test
        """
        return settings

    def assertTestEnvironment(self):
        """
        Asserts that the test environment has been loaded
        """
        self.assertEqual(settings.ENVIRONMENT, 'test')
