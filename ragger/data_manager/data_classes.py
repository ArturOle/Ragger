from typing import List, Optional
from pydantic import BaseModel


class Embeddable(BaseModel):
    embeddings: Optional[List] = None


class Literature(BaseModel):
    filename: str
    filepath: str


class Chunk(Embeddable):
    text: str
    page_number: int = 0


class Tag(Embeddable):
    text: str
    description: Optional[str] = None


class RelationWeight(BaseModel):
    literature: str
    tag: str
    weight: float


class LiteratureDTO(BaseModel):
    filename: str
    filepath: str
    text: List[str]


class LiteratureGraph(BaseModel):
    literature: Literature
    chunks: List[Chunk]
    tags: List[Tag]
    relation_weights: List[RelationWeight]