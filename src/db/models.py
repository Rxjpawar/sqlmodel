from re import S
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime
class Book(SQLModel,table=True):
    __tablename__="books"
    uid:UUID=Field(sa_column=Column(pg.UUID,primary_key=True,unique=True,default=uuid4))
    title:str
    author:str
    total_pages:int
    created_at:datetime=Field(sa_column =Column(pg.TIMESTAMP),default=datetime.now())
    updated_at:datetime=Field(sa_column =Column(pg.TIMESTAMP),default=datetime.now())

    def __repr__(self)->str:
        return f"Book=>{self.title}"