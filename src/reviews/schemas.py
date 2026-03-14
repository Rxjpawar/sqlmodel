from pydantic import BaseModel , Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class ReviewModel(BaseModel):
    uid: UUID
    review_text: str
    rating:int = Field(le=5)
    created_at: datetime
    updated_at: datetime
    user_uid:Optional[UUID]
    book_uid:Optional[UUID]

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    review_text: str
    rating:int = Field(le=5)
    