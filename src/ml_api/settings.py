from pydantic import BaseSettings


class APISettings(BaseSettings):
    API_VERSION: str = "1.0.0"

    BROKER_HOST: str = "broker"
    BROKER_PORT: int = 9092
    BROKER_TOPIC: str = "task-request"


settings = APISettings()
