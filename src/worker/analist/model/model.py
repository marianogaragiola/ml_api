"""model.py
This file contains the Machine Learning model ready to use it for predictions
"""
import numpy as np
from sentiment_analysis_spanish import sentiment_analysis

from analist.validators import SentenceSentiment
from analist.settings import (
    THRESHOLDS,
    SENTIMENTS,
    REDIS_QUEUE
)


class SentimentAnalyser():
    """
    Class used to predict the sentiment score prediction model
    """

    def __init__(self):
        self._model = sentiment_analysis.SentimentAnalysisSpanish()

    def predict(self, data: str) -> float:
        """Runs the prediction
        """
        score = self._model.sentiment(data)
        sentiment = SENTIMENTS[np.digitize(score, bins=THRESHOLDS)]
        return SentenceSentiment(
            sentence=data,
            score=score,
            sentiment=sentiment
        )

