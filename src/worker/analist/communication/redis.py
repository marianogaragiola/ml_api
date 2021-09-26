import redis

from analist.schemas import SentenceSentiment


class RedisProducer:
    _DEFAULT_TTL: int = 6000  # Time to live in seconds
    _KEY_PREFIX: str = "job_id"

    def __init__(
        self, host: str, port: int, db: int = 1
    ):
        self._conn = redis.Redis(host=host, port=port, db=db)

    def send(self, key: str, value: SentenceSentiment):
        self._conn.set(
            name=f"{self._KEY_PREFIX}:{key}",
            value=value.json(),
            ex=self._DEFAULT_TTL,
        )

