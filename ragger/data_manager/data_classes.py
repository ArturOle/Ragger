from typing import List, Optional
from pydantic import BaseModel


class Literature(BaseModel):
    filename: str
    filepath: str


class Chunk(BaseModel):
    text: str
    page_number: int = 0
    embeddings: Optional[List] = None


class Tag(BaseModel):
    name: str
    description: Optional[str] = None
    embeddings: Optional[List] = None


class RealtionWeight(BaseModel):
    Literature: Literature
    tag: Tag
    weight: float


class LiteratureDTO(BaseModel):
    filename: str
    filepath: str
    text: str
