from re import S
from sqlmodel import SQLModel, Field, Column , Relationship
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime
from typing import List
from src.db import models
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
    books:List['models.Book']=Relationship(back_populates="users",sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self)->str:
        return f"Book=>{self.username}"