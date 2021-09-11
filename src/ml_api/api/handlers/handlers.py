from typing import Callable

from fastapi import FastAPI

from ml_api.communication import KafkaSender, KafkaReader
from ml_api.settings import settings


def _startup_model(app: FastAPI) -> None:
    producer = KafkaSender(
        f"{settings.BROKER_HOST}:{settings.BROKER_PORT}",
        settings.BROKER_PRODUCER_TOPIC,
    )
    consumer = KafkaReader(
        f"{settings.BROKER_HOST}:{settings.BROKER_PORT}",
        settings.BROKER_CONSUMER_TOPIC,
    )
    consumer.start()
    app.state.producer = producer
    app.state.consumer = consumer


def _shutdown_model(app: FastAPI) -> None:
    app.state.consumer.stop()
    app.state.consumer = None
    app.state.producer = None


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
