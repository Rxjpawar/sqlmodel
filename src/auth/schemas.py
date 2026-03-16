from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing_extensions import List
from src.books.schemas import BookModel
from src.reviews.schemas import ReviewModel

class UserCreateModel(BaseModel):
    first_name:str=Field(max_length=10)
    last_name:str=Field(max_length=10)
    username:str=Field(max_length=10)
    email:str=Field(max_length=40)
    password:str=Field(max_length=10)


class UserModel(BaseModel):
    uid: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_varified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # important for SQLModel

class UserBooks(UserModel):
    books:List[BookModel]
    #review:List[ReviewModel]


class UserLoginModel(BaseModel):
    email:str=Field(max_length=40)
    password:str=Field(max_length=10)
