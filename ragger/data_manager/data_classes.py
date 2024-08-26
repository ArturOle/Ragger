from typing import List, Optional
from pydantic import BaseModel


class Literature(BaseModel):
    filename: str
    text: str
    text_position: int
    page_number: int
    keywords: Optional[List] = None
    embeddings: Optional[List] = None
