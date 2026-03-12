from re import S
from sqlmodel import SQLModel, Field, Column,Relationship
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from src.auth import models
class Book(SQLModel,table=True):
    __tablename__="books"
    uid:UUID=Field(sa_column=Column(pg.UUID,primary_key=True,unique=True,default=uuid4))
    title:str
    author:str
    total_pages:int
    user_uid:Optional[UUID]=Field(default=None,foreign_key="users.uid")
    created_at:datetime=Field(sa_column =Column(pg.TIMESTAMP),default=datetime.now())
    updated_at:datetime=Field(sa_column =Column(pg.TIMESTAMP),default=datetime.now())
    users:Optional['models.User']=Relationship(back_populates="books")

    def __repr__(self)->str:
        return f"Book=>{self.title}"