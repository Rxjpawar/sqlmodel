from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from http import HTTPStatus
from src.db.main import get_session
from src.books.service import BookService
from src.books.schemas import BookResponse, BookCreate, BookUpdate, BookDetails
from src.auth.dependencies import AccessTokenBearer, RoleCheker

book_router = APIRouter()

acess_token_bearer = AccessTokenBearer()
role_cheker = RoleCheker(["admin", "user"])


@book_router.get("/", response_model=List[BookResponse])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details=Depends(acess_token_bearer),
    _: bool = Depends(role_cheker),
):
    # print(token_details)
    books = await BookService(session).get_all_books()
    return books

@book_router.get("/user/{user_uid}", response_model=List[BookDetails])
async def get_all_books(
    user_uid:str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(acess_token_bearer),
    _: bool = Depends(role_cheker),
):
    # print(token_details)
    books = await BookService(session).get_user_books(user_uid)
    return books


@book_router.get("/{book_id}", response_model=BookResponse, status_code=HTTPStatus.OK)
async def read_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(acess_token_bearer),
    _: bool = Depends(role_cheker),
):
    book = await BookService(session).get_book(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book



@book_router.post(
    "/create", response_model=BookResponse, status_code=HTTPStatus.CREATED
)
async def create_book(
    book_create_data: BookCreate,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(acess_token_bearer),
    _: bool = Depends(role_cheker),
) -> dict:
    user_id = token_details.get("user")["user_uid"]
    new_book = await BookService(session).create_book(book_create_data, user_id)
    return new_book


@book_router.put(
    "/update/{book_id}", response_model=BookResponse, status_code=HTTPStatus.OK
)
async def update_book(
    book_id: str,
    update_data: BookUpdate,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(acess_token_bearer),
    _: bool = Depends(role_cheker),
):
    updated_book = await BookService(session).update_book(book_id, update_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@book_router.delete("/delete/{book_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(acess_token_bearer),
    _: bool = Depends(role_cheker),
):
    deleted_book = await BookService(session).delete_book(book_id)

    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return
