"""
worker.py
This file contains the Worker object that is responsible of processing
tasks or jobs enqueued in Redis
"""
import sys
import logging
from time import sleep
import json

from analist.settings import REDIS_QUEUE
from analist.model import SentimentAnalyser
from analist.communication import redis_connection


class Worker():
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

        self._logger = logging.getLogger("Redis Worker")
        self._logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.info("Initializing worker")
        self._redis_conn = redis_connection()
        self._redis_queue = REDIS_QUEUE
        self._predictor = SentimentAnalyser()

    def work(self):
        """
        Run an infinite loop that is reading task in Redis queue and
        makes the prediction with the Machine Learning model
        """
        self._logger.info("Waiting for jobs in Redis")
        while True:
            job_raw_data = self._redis_conn.lpop(self._redis_queue)
            if not job_raw_data:
                sleep(0.05)
                continue
            self._do_task(job_raw_data)
            sleep(0.05)

    def _do_task(self, raw_data):
        """
        Makes the prediction on the data read from Redis and returns the
        prediction in Redis with job_id
        """
        job_data = json.loads(raw_data)
        job_id = job_data['job_id']
        text = job_data["text"]
        self._logger.info(f"Processing job {job_id}")
        sentiment = self._predictor.predict(text)
        self._logger.info(f"Result from job {sentiment.dict()}")
        self._redis_conn.set(job_id, sentiment.json())


if __name__ == '__main__':
    worker = Worker()
    worker.work()
