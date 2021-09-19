from enum import Enum
import multiprocessing
from ipaddress import IPv4Address
from typing import Optional, Dict, Any
from pydantic import BaseSettings, PositiveInt, validator


class LoggingEnum(str, Enum):
    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class APISettings(BaseSettings):
    API_VERSION: str = "1.0.0"

    BROKER_HOST: str = "broker"
    BROKER_PORT: int = 9092
    BROKER_PRODUCER_TOPIC: str = "task-request"
    BROKER_CONSUMER_TOPIC: str = "task-computed"

    APP_MODULE: str = "ml_api.app:app"


class GunicornSettings(BaseSettings):
    """GunicornSettings Schema"""

    workers_per_core: PositiveInt = 1
    workers: Optional[PositiveInt] = None

    @validator("workers")
    def validate_workers(
        cls, v: Optional[int], values: Dict[str, Any]
    ) -> PositiveInt:
        """Validates the number of workers"""
        if isinstance(v, int):
            return v
        core_count = multiprocessing.cpu_count()
        return core_count * values.get("workers_per_core")

    worker_class: str = "uvicorn.workers.UvicornWorker"

    host: IPv4Address = "0.0.0.0"
    port: PositiveInt = 8000
    bind: Optional[str] = None

    @validator("bind", pre=True)
    def assemble_bind(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"{values.get('host')}:{values.get('port')}"

    graceful_timeout: PositiveInt = 120
    timeout: PositiveInt = 120
    keepalive: PositiveInt = 5

    # "-" logs to stdout
    accesslog: str = "-"
    errorlog: str = "-"

    loglevel: LoggingEnum = LoggingEnum.info

    class Config:
        use_enum_values = True


settings = APISettings()
gunicorn_settings = GunicornSettings()
