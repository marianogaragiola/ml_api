"""
sentiment_analysis.py
"""
import time
import logging

from fastapi import APIRouter, Request, HTTPException, status

from ml_api.api.schemas import Sentence, SentenceSentiment
from ml_api.api.models import evaluate_sentiment

router = APIRouter()


@router.post(
    "/predict",
    summary="Evaluates the sentiment of a sentence",
    description="Given a setence uses a ML model to find its setiment",
    response_model=SentenceSentiment,
    name="predict",
)
def get_sentiment(request: Request, sentence: Sentence) -> SentenceSentiment:
    """Given a sentence returns the sentence's sentiment

    Returns
    -------
    sentiment: SentenceSentiment
        Pydantic schema with the sentiment.
    """
    sentiment = evaluate_sentiment(request, sentence)
    return sentiment
