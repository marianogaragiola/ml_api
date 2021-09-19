"""analist.py
This file contains a function that creates a new taks in Redis
and waits for the results
"""
from uuid import uuid4
import json
from time import sleep
from queue import Empty

from fastapi import Request

from ml_api.settings import settings
from ml_api.api.schemas import Sentence, SentenceSentiment, TaskRequest


class ResultNotFound(Exception):
    """Exception thrown when the result could not be retrieved"""


def evaluate_sentiment(
    request: Request, sentence: Sentence
) -> SentenceSentiment:
    """
    Sends a task request to the broker and wait for the result.

    Parameters
    ----------
    request : Request
    sentece : Sentence
        The sentece to be processed

    Returns
    -------
    SentenceSentiment
    """
    producer = request.app.state.producer
    consumer = request.app.state.consumer

    task_request = TaskRequest(job_id=uuid4(), text=sentence.text)
    producer.send(
        key=task_request.job_id,
        value=task_request,
    )

    while True:
        try:
            event = consumer.query(str(task_request.job_id))
        except KeyError:
            sleep(0.01)
            continue
        if not event:
            raise ResultNotFound(
                f"Unable to retrieve output for task {task_request.job_id}"
            )
        sentiment = event
        break

    return sentiment
