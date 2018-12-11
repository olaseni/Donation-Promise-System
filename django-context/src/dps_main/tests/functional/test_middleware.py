from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from dps_main.tests import DpsTestCase
from dps_main.utilities.actions import ActionHelper
from dps_main.utilities.middleware import DPSActionsMiddleWare


class MiddlewareTestCase(DpsTestCase):

    def setUp(self):
        """
        Initialize fixtures and resources we need for tests
        """
        self.factory = RequestFactory()
        self.middleware = DPSActionsMiddleWare(lambda x: None)

    def test_action_helper(self):
        """
        GIVEN a application request object
        WHEN said middleware is operational in an app
        THEN an action helper should be automatically available in the request
        """
        request = self.factory.get('/')
        request.user = AnonymousUser()
        request.META = {}
        request.session = {}
        self.middleware(request)
        self.assertIsInstance(request.action_helper, ActionHelper)
