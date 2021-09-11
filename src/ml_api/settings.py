from pydantic import BaseSettings


class APISettings(BaseSettings):
    API_VERSION: str = "1.0.0"

    BROKER_HOST: str = "broker"
    BROKER_PORT: int = 9092
    BROKER_PRODUCER_TOPIC: str = "task-request"
    BROKER_CONSUMER_TOPIC: str = "task-computed"


settings = APISettings()
