from fastapi import APIRouter, Depends
from database import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Book
from schemas import BookCreate, BookOutput, BookUpdate
from utils import get_books_or_error_404, get_author_or_error_404


router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[BookOutput])
async def get_authors(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).limit(10))
    author = result.scalars().all()
    return author


@router.get("/{book_id}", response_model=BookOutput)
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await get_books_or_error_404(book_id, session)
    return book


@router.post("")
async def add_book(current_book: BookCreate, session: AsyncSession = Depends(get_session)):
    await get_author_or_error_404(current_book.author_id, session)
    book = Book(title=current_book.title, year=current_book.year, author_id=current_book.author_id)
    session.add(book)
    await session.commit()
    return {"detail": "Книга успешно добавлена"}


@router.patch("/{book_id}")
async def edit_book_info(
    book_id: int, current_book: BookUpdate, session: AsyncSession = Depends(get_session)
):
    book = await get_books_or_error_404(book_id, session)
    if current_book.author_id is not None:
        await get_author_or_error_404(current_book.author_id, session)
        book.author_id = current_book.author_id
    if current_book.title is not None:
        book.title = current_book.title
    if current_book.year is not None:
        book.year = current_book.year

    await session.commit()

    return {"detail": "Данные о книге успешно изменены"}


@router.delete("/{book_id}")
async def remove_book(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await get_books_or_error_404(book_id, session)
    await session.delete(book)
    await session.commit()

    return {"detail": "Книга успешно удалена"}
