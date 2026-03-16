from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from typing_extensions import List
from src.reviews.schemas import ReviewModel
class BookResponse(BaseModel):
    uid: UUID
    title: str
    author: str
    total_pages: int
    user_uid: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookDetails(BaseModel):
    review:List[ReviewModel]

class BookCreate(BaseModel):
    title:str
    author:str
    total_pages:int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    total_pages: Optional[int] = None



class BookModel(BaseModel):
    uid: UUID
    title: str
    author: str
    total_pages: int
    user_uid: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # allows building from SQLModel ORM objects