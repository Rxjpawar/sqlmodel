from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from config import settings

engine=create_async_engine(
    url=settings.DATABASE_URL,
    echo=True)

async def init_db():
    async with engine.begin() as connection:
        from .models import Book
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session