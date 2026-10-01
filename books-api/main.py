from contextlib import asynccontextmanager

from database import Base, engine, get_session
from fastapi import Depends, FastAPI, HTTPException
from models import Book
from schemas import BookCreate, BookOutput, BookUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


async def get_books_or_error_404(book_id: int, session: AsyncSession):
    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Упс! Книга не найдена")
    return book


@app.get("/books", response_model=list[BookOutput])
async def get_list_books(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).limit(10))
    books = result.scalars().all()
    return books


@app.get("/books/{book_id}", response_model=BookOutput)
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await get_books_or_error_404(book_id, session)
    return book


@app.post("/books")
async def add_book(
    current_book: BookCreate, session: AsyncSession = Depends(get_session)
):
    book = Book(
        title=current_book.title, author=current_book.author, year=current_book.year
    )
    session.add(book)
    await session.commit()
    return {"detail": "Книга успешно добавлена"}


@app.patch("/books/{book_id}")
async def edit_book_info(
    book_id: int, current_book: BookUpdate, session: AsyncSession = Depends(get_session)
):
    book = await get_books_or_error_404(book_id, session)
    if current_book.title is not None:
        book.title = current_book.title
    if current_book.author is not None:
        book.author = current_book.author
    if current_book.year is not None:
        book.year = current_book.year
    await session.commit()
    return {"detail": "Корректировки внесены успешно"}


@app.delete("/books/{book_id}")
async def remove_book(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await get_books_or_error_404(book_id, session)
    await session.delete(book)
    await session.commit()

    return {"detail": "Книга успешно удалена"}
