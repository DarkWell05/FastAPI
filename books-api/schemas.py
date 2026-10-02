from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=3, max_length=90)
    author_id: int
    year: int = Field(ge=1, le=2030)


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=90)
    author_id: int | None = None
    year: int | None = Field(default=None, ge=1, le=2030)


class BookOutput(BaseModel):
    id: int
    title: str
    author_id: int
    year: int
    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class AuthorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)


class AuthorOutput(BaseModel):
    id: int
    name: str
    model_config=ConfigDict(from_attributes=True)
