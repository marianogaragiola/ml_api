"""
sentiment_analysis.py
"""
import time
import logging

from fastapi import APIRouter, Request, status, HTTPException

from ml_api.api.schemas import Sentence, SentenceSentiment, Message
from ml_api.api.models import evaluate_sentiment, ResultNotFound

router = APIRouter()


@router.post(
    "/predict",
    summary="Evaluates the sentiment of a sentence",
    description="Given a setence uses a ML model to find its setiment",
    response_model=SentenceSentiment,
    responses={status.HTTP_400_BAD_REQUEST: {"model": Message}},
    name="predict",
)
def get_sentiment(request: Request, sentence: Sentence) -> SentenceSentiment:
    """Given a sentence returns the sentence's sentiment

    Returns
    -------
    sentiment: SentenceSentiment
        Pydantic schema with the sentiment.
    """
    try:
        sentiment = evaluate_sentiment(request, sentence)
    except ResultNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        ) from exc
    return sentiment
