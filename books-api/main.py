from contextlib import asynccontextmanager

from database import engine, Base
from fastapi import FastAPI
from routers import authors, books

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(authors.router)
app.include_router(books.router)
