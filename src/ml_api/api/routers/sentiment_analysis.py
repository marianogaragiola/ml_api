"""
sentiment_analysis.py
"""
import time
import logging
from typing import Optional

from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ml_api.api.schemas import Sentence, SentenceSentiment, Message
from ml_api.api.models import evaluate_sentiment, ResultNotFound

router = APIRouter()
router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="/app/ml_api/templates")


@router.get(
    "/",
    summary="Serves a static file in the browser",
    response_class=HTMLResponse,
)
def ui(request: Request, text: Optional[str] = None):
    html_info = {"request": request}
    if text:
        prediction = evaluate_sentiment(request, Sentence(text=text))
        html_info.update({"sentiment": prediction.sentiment})
        html_info.update({"score": prediction.score})
    return templates.TemplateResponse("index.html", html_info)


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
            status_code=status.HTTP_404_NOT_FOUND
        ) from exc
    return sentiment
