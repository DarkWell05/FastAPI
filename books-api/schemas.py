from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=3, max_length=90)
    author: str = Field(min_length=3, max_length=50)
    year: int = Field(ge=1, le=2030)


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=90)
    author: str | None = Field(default=None, min_length=3, max_length=50)
    year: int | None = Field(default=None, ge=1, le=2030)


class BookOutput(BaseModel):
    id: int
    title: str
    author: str
    year: int
    model_config = ConfigDict(from_attributes=True)
