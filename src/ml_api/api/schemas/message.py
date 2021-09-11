from pydantic import BaseModel


class Message(BaseModel):
    """Simple schema to represent a message."""

    message: str
