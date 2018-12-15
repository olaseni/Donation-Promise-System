from random import randint

from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from dps_main.tests import DpsTestCase
from dps_main.utilities import faker

from dps_main.views.views import CausesListView


@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
})
class APITestCase(DpsTestCase):
    """
    Web views
    """

    def setUp(self):
        """
        Initialize fixtures and resources we need for tests
        """
        self.users = dict(user=faker.user(True, password='020202')[1], super=faker.user(True, True)[1])
        faker.bulk_causes(15, self.users['super'])

    def test_anonymous_home(self):
        """
        GIVEN our site
        WHEN requested
        THEN certain string should be in the content
        """
        response = self.client.get('/', follow=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, text='promise', count=CausesListView.paginate_by + 1)

    def test_login(self):
        """
        GIVEN our site
        WHEN login is requested
        THEN it should succeed
        """
        self.client.login(**{
            'username': self.users['user'].username,
            'password': '020202'
        })
        response = self.client.get(reverse('login'), follow=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.users['user'].pk)

    def test_register(self):
        """
        GIVEN our site
        WHEN registration is requested
        THEN It should succeed
        """

        username = 'lola-{}'.format(randint(2, 342323))
        password = 'wicker-{}'.format(randint(224343, 3423239999))
        response = self.client.post(reverse('register'), {
            'username': username,
            'password1': password,
            'password2': password
        }, follow=True, format='form')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(User.objects.get(username=username), User)
