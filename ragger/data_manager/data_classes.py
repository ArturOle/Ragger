from typing import List, Optional
from pydantic import BaseModel


class Literature(BaseModel):
    title: str
    text: str
    authors: Optional[List] = None
    summary: Optional[str] = None
