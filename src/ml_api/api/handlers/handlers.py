from typing import Callable

from fastapi import FastAPI

from ml_api.communication import KafkaSender, RedisConsumer
from ml_api.settings import settings


def _startup_model(app: FastAPI) -> None:
    producer = KafkaSender(
        f"{settings.BROKER_HOST}:{settings.BROKER_PORT}",
        settings.BROKER_PRODUCER_TOPIC,
    )
    redis_conn = RedisConsumer(
        settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB
    )
    app.state.producer = producer
    app.state.connection = redis_conn


def _shutdown_model(app: FastAPI) -> None:
    app.state.producer = None
    app.state.connections = None


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        print("Running app start handler.")
        _startup_model(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        print("Running app shutdown handler.")
        _shutdown_model(app)

    return shutdown
