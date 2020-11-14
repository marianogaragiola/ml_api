from pydantic import BaseModel


class Sentence(BaseModel):
    text: str

    class Config:
        schema_extra = {
            'example': {
                'text': 'Some text'
            }
        }


class SentenceSentiment(BaseModel):
    sentence: str
    score: float
    sentiment: str

    class Config:
        schema_extra = {
            'example': {
                'sentence': {
                    'text': 'Some text'
                },
                'score': 0.643,
                'sentimente': 'neutral'
            }
        }
