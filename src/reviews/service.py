from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from src.reviews.schemas import ReviewCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException 
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError

class ReviewService():
    def __init__(self,session:AsyncSession):
        self.session = session
        self.user_service = UserService(session)
        self.book_service = BookService(session)

    async def add_reviews_too_book(self,user_email:str,book_uid:str,review_data:ReviewCreate):
        try:
            book  = await self.book_service.get_book(book_uid)
            user = await self.user_service.get_user_by_email(user_email)

            new_review = Review(**review_data.model_dump())

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
            
            if not book:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found")

            new_review.users = user
            new_review.books = book

            self.session.add(new_review)
            await self.session.commit()
            await self.session.refresh(new_review)
            return new_review

        except HTTPException:
            raise
        except SQLAlchemyError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="database error while adding review",
            )
        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="failed to add review",
            )