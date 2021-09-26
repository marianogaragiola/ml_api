"""
worker.py
This file contains the Worker object that is responsible of processing
tasks or jobs enqueued in Redis
"""
import sys
import logging
from time import sleep
import json

from analist.settings import settings
from analist.model import SentimentAnalyser
from analist.communication import ConsumerBuilder, KafkaSender, RedisProducer
from analist.schemas import TaskRequest, SentenceSentiment


class Worker:
    """
    Class responsible for processing task in redis.

    Methods:
    -------
    work
    """

    def __init__(self):
        """
        Class constructor
        """

        self._logger = logging.getLogger("Worker")
        self._logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.info("Initializing worker")
        self._consumer = ConsumerBuilder.build(
            broker_url=f"{settings.BROKER_HOST}:{settings.BROKER_PORT}",
            topic=settings.BROKER_CONSUMER_TOPIC,
            group_id=settings.BROKER_GROUP_ID,
        )
        self._producer = RedisProducer(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
        )
        self._predictor = SentimentAnalyser()

    def work(self):
        """
        Run an infinite loop that is reading task in Redis queue and
        makes the prediction with the Machine Learning model
        """
        self._logger.info("Waiting for task event in Broker")
        for task_event in self._consumer:
            self._logger.info(f"Processing job {task_event.value.job_id}")
            prediction = self._do_task(task_event.value)
            self._logger.info(f"Result from job {prediction.dict()}")
            self._producer.send(key=task_event.key, value=prediction)

    def _do_task(self, data: TaskRequest) -> SentenceSentiment:
        """
        Makes a prediction on the data
        """
        sentiment = self._predictor.predict(data.text)
        return sentiment


if __name__ == "__main__":
    worker = Worker()
    worker.work()
