from kafka import KafkaProducer

from ml_api.settings import settings


def create_kafka_producer() -> KafkaProducer:
    """Creates a Kafka producer

    Returns
    -------
    KafkaProducer
    """
    host = settings.BROKER_HOST
    port = settings.BROKER_PORT
    broker_url = f"{host}:{port}"
    producer = KafkaProducer(bootstrap_servers=broker_url)
    return producer
