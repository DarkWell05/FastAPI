from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    books: Mapped[list["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int] 
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author : Mapped["Author"] = relationship(back_populates="books")
