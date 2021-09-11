from uuid import UUID

from pydantic import BaseModel


class TaskRequest(BaseModel):
    job_id: UUID
    text: str


class Sentence(BaseModel):
    text: str

    class Config:
        schema_extra = {"example": {"text": "Some text"}}


class SentenceSentiment(BaseModel):
    sentence: str
    score: float
    sentiment: str

    class Config:
        schema_extra = {
            "example": {
                "sentence": "Some text",
                "score": 0.643,
                "sentimente": "neutral",
            }
        }
