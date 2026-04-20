from pydantic import BaseModel
from typing import List, Optional

class Ebook(BaseModel):
    title: str
    author: str
    category: str
    tags: List[str]
    file_url: str
    cover_url: str
