from mockredis import mock_redis_client


def mock_redis(*args, **kwargs):
    """
    Patching the stock MockRedis object to meet third-party app expectations
    """
    mrc = mock_redis_client()
    mrc.close = lambda: None
    return mrc
