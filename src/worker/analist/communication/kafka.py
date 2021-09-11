import json
from uuid import UUID
from typing import Optional

from kafka import KafkaProducer, KafkaConsumer
from pydantic import BaseModel

from analist.schemas import TaskRequest, SentenceSentiment


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
    return json.dumps(value.dict(), default=lambda x: str(x)).encode()


def value_message_deserializer(value: bytes) -> TaskRequest:
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
    return TaskRequest.parse_obj(decoded)


class ConsumerBuilder:
    @staticmethod
    def build(
        broker_url: str, topic: str, group_id: Optional[str] = None
    ) -> KafkaConsumer:
        """builds a Kafka Consumer.

        Parameters
        ----------
        broker_url : str
            broker_url
        topic : str
            topic
        group_id : Optional[str]
            group_id

        Returns
        -------
        KafkaConsumer
        """
        consumer = KafkaConsumer(
            topic,
            group_id=group_id,
            bootstrap_servers=broker_url,
            auto_offset_reset="latest",
            enable_auto_commit=True,
            value_deserializer=value_message_deserializer,
            key_deserializer=lambda x: x.decode(),
        )
        return consumer


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
        self._producer = KafkaProducer(
            bootstrap_servers=broker_url, value_serializer=value_serializer
        )

    def send(self, key: UUID, value: SentenceSentiment):
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
