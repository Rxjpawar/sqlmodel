from re import S
from sqlmodel import SQLModel, Field, Column,Relationship
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from typing import List

#User related models
class User(SQLModel,table=True):
    __tablename__="users"
    uid:UUID=Field(sa_column=Column(pg.UUID,primary_key=True,unique=True,default=uuid4))
    username:str
    email:str
    first_name:str
    last_name:str
    is_varified: bool=False
    password_hash:str=Field(exclude=False)
    role:str = Field(sa_column=Column(pg.VARCHAR,nullable=False,server_default="user"))
    created_at:datetime=Field(sa_column =Column(pg.TIMESTAMP),default=datetime.now())
    updated_at:datetime=Field(sa_column =Column(pg.TIMESTAMP),default=datetime.now())
    books:List['Book']=Relationship(back_populates="users",sa_relationship_kwargs={"lazy":"selectin"})
    reviews:List['Review']=Relationship(back_populates="users",sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self)->str:
        return f"Book=>{self.username}"

#Books related models
class Book(SQLModel,table=True):
    __tablename__="books"
    uid:UUID=Field(sa_column=Column(pg.UUID,primary_key=True,unique=True,default=uuid4))
    title:str
    author:str
    total_pages:int
    user_uid:Optional[UUID]=Field(default=None,foreign_key="users.uid")
    created_at:datetime=Field(sa_column =Column(pg.TIMESTAMP),default=datetime.now())
    updated_at:datetime=Field(sa_column =Column(pg.TIMESTAMP),default=datetime.now())
    users:Optional['User']=Relationship(back_populates="books")
    reviews:List['Review']=Relationship(back_populates="books",sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self)->str:
        return f"Book=>{self.title}"
    
class Review(SQLModel,table=True):
    __tablename__="reviews"
    uid:UUID=Field(sa_column=Column(pg.UUID,primary_key=True,unique=True,default=uuid4))
    rating:int=Field(le=5)
    review_text:str
    user_uid:Optional[UUID]=Field(default=None,foreign_key="users.uid")
    book_uid:Optional[UUID]=Field(default=None,foreign_key="books.uid")
    created_at:datetime=Field(sa_column =Column(pg.TIMESTAMP),default=datetime.now())
    updated_at:datetime=Field(sa_column =Column(pg.TIMESTAMP),default=datetime.now())
    users:Optional['User']=Relationship(back_populates="reviews")
    books:Optional['Book']=Relationship(back_populates="reviews")

    def __repr__(self)->str:
        return f"Review for book {self.book_uid} by user {self.user_uid}"
    
