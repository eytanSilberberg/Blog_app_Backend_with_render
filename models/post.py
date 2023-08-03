from typing import Optional
from pydantic import BaseModel


class Post(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    image: str


class PostToSave(BaseModel):
    title: str
    description: str
    image: str
