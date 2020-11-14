from typing import Callable

from fastapi import FastAPI

from ml_api.communication import redis_connection


def _startup_model(app: FastAPI) -> None:
    connection = redis_connection()
    app.state.connection = connection


def _shutdown_model(app: FastAPI) -> None:
    app.state.redis = None


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

