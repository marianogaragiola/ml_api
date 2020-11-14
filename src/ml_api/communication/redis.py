import redis

from ml_api.settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB
)


def redis_connection():
    """
    Connects to Redis DB and returns the connection
    """
    conn = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB
    )
    return conn
