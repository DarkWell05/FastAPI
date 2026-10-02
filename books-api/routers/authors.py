from fastapi import APIRouter, Depends, HTTPException
from schemas import AuthorCreate, AuthorUpdate, AuthorOutput, AuthorWithBooks
from sqlalchemy.orm import selectinload
from database import get_session
from sqlalchemy import select
from models import Author
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_author_or_error_404


router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("", response_model=list[AuthorOutput])
async def get_authors(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Author).limit(10))
    author = result.scalars().all()
    return author

@router.get("/{author_id}", response_model=AuthorWithBooks)
async def get_author_and_him_books(author_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Author).where(Author.id == author_id).options(selectinload(Author.books)))
    author = result.scalar_one_or_none()
    if author is None:
        raise HTTPException(status_code=404, detail="Упс! Автор не найден")
    return author

@router.post("")
async def add_author(current_author: AuthorCreate, session: AsyncSession = Depends(get_session)):
    author = Author(name=current_author.name)

    session.add(author)
    await session.commit()
    return {"detail": "Автор успешно добавлен"}
    

@router.patch("/{author_id}")
async def rename_author(author_id: int, current_author: AuthorUpdate, session: AsyncSession = Depends(get_session)):
    author = await get_author_or_error_404(author_id, session)
    if current_author.name is not None:
        author.name = current_author.name

    await session.commit()
    return {"detail": "Данные об авторе успешно изменены"}


@router.delete("/{author_id}")
async def remove_author(author_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Author).where(Author.id == author_id).options(selectinload(Author.books)))
    author = result.scalar_one_or_none()
    if author is None:
        raise HTTPException(status_code=404, detail="Упс! Автор не найден")
    
    await session.delete(author)
    await session.commit()
    return {"detail": "Автор и его книги успешно удалены"}
    
