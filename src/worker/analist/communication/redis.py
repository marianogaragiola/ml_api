import redis

from analist.settings import settings


def redis_connection():
    """
    Connects to Redis DB and returns the connection
    """
    conn = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )
    return conn
