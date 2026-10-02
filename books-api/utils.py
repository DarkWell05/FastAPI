from fastapi import HTTPException
from models import Book, Author
from sqlalchemy.ext.asyncio import AsyncSession

async def get_books_or_error_404(book_id: int, session: AsyncSession):
    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Упс! Книга не найдена")
    return book


async def get_author_or_error_404(author_id: int, session: AsyncSession):
    author = await session.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Упс! Автор не найден")
    return author
