import json
from typing import Dict

import redis
from retry import retry


class ValueNotFound(Exception):
    pass


class RedisConsumer:

    _PREFIX: str = "job_id"

    def __init__(self, host: str, port: int, db: int = 0):

        self._conn = redis.Redis(host=host, port=port, db=db)

    @retry(ValueNotFound, tries=20, delay=0.01)
    def get(self, job_id: str) -> Dict:
        output = self._conn.get(f"{self._PREFIX}:{job_id}")
        if output is None:
            raise ValueNotFound(f"Job {job_id} not found in database")
        return json.loads(output)
