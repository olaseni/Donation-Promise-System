import redis
from unittest.mock import patch
from django.test import TestCase
from mockredis import mock_redis_client, mock_strict_redis_client


class RedisTestCase(TestCase):
    """
    A test case to test that the redis setup is sound
    """

    redis = None

    @classmethod
    @patch('redis.StrictRedis', mock_strict_redis_client)
    @patch('redis.Redis', mock_redis_client)
    def setUpClass(cls):
        """
        Setup the redis client connection at startup
        """
        super().setUpClass()
        cls.redis = redis.Redis(host='redis')

    def setUp(self):
        """
        Sets a key value pre-test
        """
        self.redis.set('one', 1)

    def test_key(self):
        """
        GIVEN a previously set key
        WHEN that key is retrieved later
        THEN the value in that key should yield expected results
        """
        self.assertEqual(int(self.redis.get('one')), 1)

    def test_misc(self):
        """
        GIVEN a retinue of set and retrieval conditions
        WHEN a key is set or a list is appended to
        THEN values in those containers should yield expected results
        """
        self.assertEqual(len(self.redis.keys('one')), 1)
        self.redis.delete('one')
        self.assertEqual(len(self.redis.keys('one')), 0)
        self.redis.lpush('two', 1, 2, 3, 4, 5)
        self.assertEqual(len(self.redis.keys('two')), 1)
        self.assertEqual(len(self.redis.lrange('two', -100, 100)), 5)
        self.redis.delete('two')

    @classmethod
    def tearDownClass(cls):
        """
        Flush all keys. This is important to make tests sane
        """
        if not isinstance(cls.redis, redis.Redis):
            cls.redis.flushdb()
        cls.redis = None
        super().tearDownClass()
