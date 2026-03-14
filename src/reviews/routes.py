from fastapi import APIRouter
from src.reviews.schemas import ReviewCreate
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.reviews.service import ReviewService
from src.auth.dependencies import get_current_user
from src.db.models import User

reviews_router = APIRouter()

@reviews_router.post("/book/{book_id}")
async def add_review_to_books(
    book_id: str,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await ReviewService(session).add_reviews_too_book(
        user_email=current_user.email,
        book_uid=book_id,
        review_data=review_data,
    )
    return new_review
