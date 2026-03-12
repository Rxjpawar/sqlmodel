from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from src.books.schemas import BookCreate, BookUpdate


class BookService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self):
        statement = select(Book).order_by(Book.created_at)
        result = await self.session.execute(statement)
        return result.scalars().all()
    
    async def get_user_books(self,user_uid:str):
        statement = select(Book).where(Book.user_uid==user_uid).order_by(Book.created_at)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_book(self, book_uid: str):
        statement = select(Book).where(Book.uid == book_uid)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_book(self, book_data: BookCreate, user_uid: str):
        new_book = Book(**book_data.model_dump())
        new_book.user_uid= user_uid
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book

    async def update_book(self, book_uid: str, book_update_data: BookUpdate):
        statement = select(Book).where(Book.uid == book_uid)
        result = await self.session.execute(statement)
        updated_book = result.scalar_one_or_none()

        if not updated_book:
            return None
        update_data = book_update_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(updated_book, key, value)

        await self.session.commit()
        await self.session.refresh(updated_book)

        return updated_book

    async def delete_book(self, book_uid: str):
        statement = select(Book).where(Book.uid == book_uid)
        result = await self.session.execute(statement)
        book = result.scalar_one_or_none()

        if not book:
            return None
        await self.session.delete(book)
        await self.session.commit()

        return book
