import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWD

connection_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWD, decode_responses=True,
                                       retry_on_timeout=5, max_connections=1024)


def get_session():
    return redis.Redis(connection_pool=connection_pool)
