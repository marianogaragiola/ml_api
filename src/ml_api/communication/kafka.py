import json
import time
from uuid import UUID
from typing import Optional
from threading import Thread

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from ml_api.api.schemas import SentenceSentiment


def value_serializer(value: BaseModel) -> bytes:
    """Serilizer for a new message

    Parameters
    ----------
    value : BaseModel
        value

    Returns
    -------
    bytes

    """
    return json.dumps(jsonable_encoder(value)).encode()


def value_message_deserializer(value: bytes) -> SentenceSentiment:
    """Deserializer for the message value in kafka

    Parameters
    ----------
    value : bytes
        value

    Returns
    -------
    TaskRequest
    """
    decoded = json.loads(value.decode())
    return SentenceSentiment.parse_obj(decoded)


class KafkaReader:
    def __init__(
        self,
        broker_url: str,
        topic: str,
        group_id: Optional[str] = None,
        max_elements: Optional[int] = 1000,
    ):

        self._consumer = KafkaConsumer(
            topic,
            group_id=group_id,
            bootstrap_servers=broker_url,
            auto_offset_reset="latest",
            enable_auto_commit=True,
            value_deserializer=value_message_deserializer,
            key_deserializer=lambda x: x.decode(),
        )
        self._thread = Thread(target=self._consume, daemon=True)
        self._msg_queue = {}

    def start(self):
        self._thread.start()

    def stop(self):
        self._consumer.close()
        self._thread.join(timeout=1.0)

    def _consume(self):
        for msg in self._consumer:
            self._msg_queue[msg.key] = msg.value

    def query(self, key: str):
        return self._msg_queue.pop(key)


class KafkaSender:
    """Wraper for a kafka producer"""

    def __init__(self, broker_url: str, topic: str):
        """Class constructor

        Parameters
        ----------
        broker_url : str
            broker_url
        topic : str
            topic
        """

        self._topic = topic
        self._producer = self._create_producer(broker_url, topic)

    @staticmethod
    def _create_producer(broker_url: str, topic: str) -> KafkaProducer:
        while True:
            try:
                print("Creating Kafka Producer")
                producer = KafkaProducer(
                    bootstrap_servers=broker_url, value_serializer=value_serializer
                )
            except NoBrokersAvailable as exc:
                time.sleep(0.5)
                continue
            finally:
                break

        return producer

    def send(self, key: UUID, value):
        """sends a new message to kafka topic.

        Parameters
        ----------
        key : UUID
            key
        value : SentenceSentiment
            value
        """
        self._producer.send(self._topic, key=str(key).encode(), value=value)
        self._producer.flush()


# def create_kafka_producer() -> KafkaProducer:
# """Creates a Kafka producer

# Returns
# -------
# KafkaProducer
# """
# host = settings.BROKER_HOST
# port = settings.BROKER_PORT
# broker_url = f"{host}:{port}"
# producer = KafkaProducer(bootstrap_servers=broker_url)
# return producer
