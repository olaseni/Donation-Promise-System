from random import choice
from io import BytesIO
from datetime import datetime, date
from json import JSONEncoder
from base64 import b64encode

from PIL import Image

from django.test.utils import override_settings
from rest_framework import status

from dps_main.tests import DpsTestCase
from dps_main.utilities import faker
from dps_main.utilities.actions import ActionHelper


class JSONEncoderPlus(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, date):
            return o.isoformat()

        return JSONEncoder.default(self, o)


@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
})
class APITestCase(DpsTestCase):

    def setUp(self):
        """
        Initialize fixtures and resources we need for tests
        """
        self.users = dict(user=faker.user(True)[1], super=faker.user(True, True)[1])
        self.action_helper_super = ActionHelper(self.users['super'])
        faker.bulk_causes(5, self.users['super'])
        self.cause_ids = [qi[0] for qi in self.action_helper_super.list_causes().values_list('id')]

        from rest_framework.test import APIClient
        self.api_client = APIClient()

    def tearDown(self):
        self.api_client.logout()
        self.action_helper_super.list_causes().delete()

    @property
    def random_cause_id(self):
        return choice(self.cause_ids)

    @property
    def random_image(self):
        bio = BytesIO()
        image = Image.new("RGB", (200, 200), 'green')
        image.save(bio, 'JPEG', compress_level=0, optimize=False)
        return bio

    @property
    def random_image_64(self):
        return b64encode(self.random_image.getvalue()).decode()

    def test_cause_get_list_unauthenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `un-authed` GET request is made to causes root
        THEN valid data should be returned when user is unauthenticated
        """
        request = self.api_client.get('/api/v1/cause/')
        self.assertIsInstance(request.data, dict)
        self.assertIsInstance(request.data['results'], list)
        self.assertEqual(len(request.data['results']), 5)

    def test_cause_get_list_authenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `authed` GET request is made to causes root
        THEN valid data should be returned when user is authenticated
        """
        self.api_client.force_login(self.users['user'])
        request = self.api_client.get('/api/v1/cause/')
        self.assertIsInstance(request.data, dict)
        self.assertIsInstance(request.data['results'], list)
        self.assertEqual(len(request.data['results']), 5)
        # test available causes
        request = self.api_client.get('/api/v1/cause/available/')
        self.assertIsInstance(request.data, dict)
        self.assertIsInstance(request.data['results'], list)
        self.assertEqual(len(request.data['results']), 5)

    def test_cause_get_detail_unauthenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `un-authed` GET request is made to causes detail
        THEN read should happen
        """
        cid = self.random_cause_id
        request = self.api_client.get('/api/v1/cause/{}/'.format(cid))
        self.assertIsInstance(request.data, dict)
        self.assertEqual(request.data['id'], cid)

    def test_cause_get_detail_authenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `authed` GET request is made to causes detail
        THEN read should happen
        """
        cid = self.random_cause_id
        self.api_client.force_login(self.users['user'])
        request = self.api_client.get('/api/v1/cause/{}/'.format(cid))
        self.assertIsInstance(request.data, dict)
        self.assertEqual(request.data['id'], cid)

    def test_cause_post_detail_unauthenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `un-authed` POST request is made to causes detail
        THEN an error should occur
        """
        memory_cause = faker.cause()[0]
        memory_cause['illustration'] = self.random_image_64
        request = self.api_client.post('/api/v1/cause/', data=memory_cause)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_cause_post_detail_authenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `authed` POST request is made to causes
        THEN a write should occur
        """
        memory_cause = faker.cause()[0]
        memory_cause['illustration'] = self.random_image_64
        self.api_client.force_login(self.users['super'])
        request = self.api_client.post('/api/v1/cause/', data=memory_cause)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_cause_put_detail_unauthenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `un-authed` PUT request is made to causes
        THEN an error should occur
        """
        cid = self.random_cause_id
        memory_cause = faker.cause()[0]
        memory_cause['illustration'] = self.random_image_64
        request = self.api_client.put('/api/v1/cause/{}/'.format(cid), data=memory_cause)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_cause_put_detail_authenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `authed` PUT request is made to causes detail
        THEN a write should occur
        """
        cid = self.random_cause_id
        memory_cause = faker.cause()[0]
        memory_cause['illustration'] = self.random_image_64
        self.api_client.force_login(self.users['super'])
        request = self.api_client.put('/api/v1/cause/{}/'.format(cid), data=memory_cause)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_cause_delete_detail_unauthenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `un-authed` DELETE request is made to causes
        THEN an error should occur
        """
        cid = self.random_cause_id
        request = self.api_client.delete('/api/v1/cause/{}/'.format(cid))
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_cause_delete_detail_authenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `authed` DELETE request is made to causes detail
        THEN a deletion should occur
        """
        cid = self.random_cause_id
        self.api_client.force_login(self.users['super'])
        request = self.api_client.delete('/api/v1/cause/{}/'.format(cid))
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_promise_post_detail_unauthenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `un-authed` POST request is made to promises
        THEN an error should occur
        """
        cid = self.random_cause_id
        request = self.api_client.post('/api/v1/promise/{}/make/'.format(cid))
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_promise_post_detail_authenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `authed` POST request is made to promises
        THEN a write should occur
        """
        cid = self.random_cause_id
        self.api_client.force_login(self.users['user'])
        data = {'amount': 30, 'target_date': date.today()}
        request = self.api_client.post('/api/v1/promise/{}/make/'.format(cid), data=data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_promise_delete_detail_unauthenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `un-authed` DELETE request is made to promises
        THEN an error should occur
        """
        promise = faker.make_promise(create=True, user=self.users['user'], cause=self.random_cause_id,
                                     amount=400)[1]
        request = self.api_client.delete('/api/v1/promise/{}/'.format(promise.id))
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_promise_delete_detail_authenticated(self):
        """
        GIVEN a request-worthy api
        WHEN an `authed` DELETE request is made to promise detail
        THEN a deletion should occur
        """
        promise = faker.make_promise(create=True, user=self.users['user'], cause=self.random_cause_id,
                                     amount=400)[1]
        self.api_client.force_login(self.users['super'])
        request = self.api_client.delete('/api/v1/promise/{}/'.format(promise.id))
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
