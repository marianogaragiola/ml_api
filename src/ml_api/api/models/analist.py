"""analist.py
This file contains a function that creates a new taks in Redis
and waits for the results
"""
from uuid import uuid4
import json
from time import sleep

from fastapi import Request

from ml_api.settings import REDIS_QUEUE
from ml_api.api.validators import Sentence, SentenceSentiment


def evaluate_sentiment(request: Request, sentence: Sentence):
    """
    Sends the job to Redis queue and waits for the result.
    """
    conn = request.app.state.connection

    job_id = str(uuid4())
    data = {
        "job_id": job_id,
        "text": sentence.text
    }
    conn.rpush(
        REDIS_QUEUE,
        json.dumps(data)
    )

    while True:
        result = conn.get(job_id)
        if result is not None:
            result = json.loads(result)
            conn.delete(job_id)
            break
        sleep(0.05)
    sentiment = SentenceSentiment(**result)
    return sentiment
