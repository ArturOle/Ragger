from typing import List, Optional
from pydantic import BaseModel


class Literature(BaseModel):
    filename: str
    text: str
    text_position: int = 0
    page_number: int = 0
    keywords: Optional[List] = None
    embeddings: Optional[List] = None
