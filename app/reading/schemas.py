from pydantic import BaseModel

class BookmarkCreate(BaseModel):
    ebook_id: str
    page_number: int

class NoteCreate(BaseModel):
    ebook_id: str
    page_number: int
    content: str
