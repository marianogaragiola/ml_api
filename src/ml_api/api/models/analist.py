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
from ml_api.communication import ValueNotFound
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
    consumer = request.app.state.connection

    task_request = TaskRequest(job_id=uuid4(), text=sentence.text)
    producer.send(
        key=task_request.job_id,
        value=task_request,
    )

    try:
        job_result = consumer.get(task_request.job_id)
    except ValueNotFound as exc:
        raise ResultNotFound from exc
    sentiment = SentenceSentiment.parse_obj(job_result)
    return sentiment
