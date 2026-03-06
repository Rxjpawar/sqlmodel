from pydantic import BaseModel , Field
from typing import Optional
from src.db.models import Book

class BookResponse(Book):
    pass

class BookCreate(BaseModel):
    title:str
    author:str
    total_pages:int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    total_pages: Optional[int] = None