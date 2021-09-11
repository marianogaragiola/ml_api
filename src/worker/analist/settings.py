from typing import List
from pydantic import BaseSettings


class WorkerSettings(BaseSettings):

    BROKER_HOST: str = "broker"
    BROKER_PORT: int = 9092
    BROKER_CONSUMER_TOPIC: str = "task-request"
    BROKER_PRODUCER_TOPIC: str = "task-computed"

    THRESHOLDS: List[float] = [0.25, 0.75]
    SENTIMENTS: List[str] = ["negative", "neutral", "positive"]

    REDIS_HOST = "redis"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_QUEUE = "service_queue"


settings = WorkerSettings()
