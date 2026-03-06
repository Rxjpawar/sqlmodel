from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from http import HTTPStatus
from src.db.main import get_session
from src.books.service import BookService
from src.books.schemas import BookResponse, BookCreate, BookUpdate

book_router = APIRouter()


@book_router.get("/", response_model=List[BookResponse])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    return await BookService(session).get_all_books()


@book_router.get("/{book_id}", response_model=BookResponse, status_code=HTTPStatus.OK)
async def read_book(book_id: str, session: AsyncSession = Depends(get_session)):
    book = await BookService(session).get_book(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@book_router.post("/create",response_model=BookResponse,status_code=HTTPStatus.CREATED)
async def create_book(book_create_data: BookCreate,session: AsyncSession = Depends(get_session)):
    return await BookService(session).create_book(book_create_data)


@book_router.put("/update/{book_id}",response_model=BookResponse,status_code=HTTPStatus.OK)
async def update_book(book_id: str,update_data: BookUpdate,session: AsyncSession = Depends(get_session)):
    updated_book = await BookService(session).update_book(book_id, update_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@book_router.delete("/delete/{book_id}",status_code=HTTPStatus.NO_CONTENT)
async def delete_book(book_id: str,session: AsyncSession = Depends(get_session)):
    deleted_book = await BookService(session).delete_book(book_id)

    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return