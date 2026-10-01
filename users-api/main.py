from contextlib import asynccontextmanager

from database import Base, SessionLocal, engine, get_session
from fastapi import Depends, FastAPI, HTTPException
from models import User
from schemas import UserCreate, UserOut, UserUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    # создаём таблицы по реестру Base.metadata
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # кладём одного пользователя, чтобы было что читать
    async with SessionLocal() as session:
        result = await session.execute(select(User).limit(1))
        if result.scalar_one_or_none() is None:
            session.add(User(name="Вася", email="vasya@example.com", age=16))
            session.add(User(name="Эльвин", email="elvin@example.com", age=18))
            await session.commit()

    yield  # тут сервер работает


app = FastAPI(lifespan=lifespan)


async def get_user_or_error_404(user_id: int, session: AsyncSession) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user_or_error_404(user_id, session)
    return user


@app.get("/users", response_model=list[UserOut])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).limit(10))
    users = result.scalars().all()
    return users


@app.post("/users", response_model=UserOut)
async def add_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(name=data.name, email=data.email, age=data.age)
    session.add(user)
    await session.commit()
    return user


@app.delete("/users/{user_id}")
async def remove_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user_or_error_404(user_id, session)
    await session.delete(user)
    await session.commit()
    return {"detail": "Пользователь удален"}


@app.patch("/users/{user_id}", response_model=UserOut)
async def change_data_user(
    user_id: int, data: UserUpdate, session: AsyncSession = Depends(get_session)
):
    user = await get_user_or_error_404(user_id, session)
    if data.name is not None:
        user.name = data.name
    if data.email is not None:
        user.email = data.email
    if data.age is not None:
        user.age = data.age

    await session.commit()
    return user
