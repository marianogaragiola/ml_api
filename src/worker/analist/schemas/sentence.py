from uuid import UUID
from pydantic import BaseModel


class SentenceSentiment(BaseModel):
    sentence: str
    score: float
    sentiment: str

    class Config:
        schema_extra = {
            "example": {
                "sentence": {"text": "Some text"},
                "score": 0.643,
                "sentimente": "neutral",
            }
        }


class TaskRequest(BaseModel):
    job_id: UUID
    text: str
