"""analist.py
This file contains a function that creates a new taks in Redis
and waits for the results
"""
from uuid import uuid4
import json
from time import sleep

from fastapi import Request
from fastapi.encoders import jsonable_encoder

from ml_api.settings import settings
from ml_api.api.schemas import Sentence, SentenceSentiment, TaskRequest


def evaluate_sentiment(request: Request, sentence: Sentence):
    """
    Sends the job to Redis queue and waits for the result.
    """
    producer = request.app.state.producer

    task_request = TaskRequest(job_id=uuid4(), text=sentence.text)
    producer.send(
        settings.BROKER_TOPIC,
        key=str(task_request.job_id).encode(),
        value=json.dumps(jsonable_encoder(task_request)).encode(),
    )
    producer.flush()

    result = {
        "sentence": "text",
        "score": 0.5,
        "sentiment": "neutral",
    }
    sentiment = SentenceSentiment(**result)
    return sentiment
