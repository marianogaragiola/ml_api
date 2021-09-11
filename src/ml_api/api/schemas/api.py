from pydantic import BaseModel


class ApiVersionModel(BaseModel):
    title: str
    description: str
    version: str
