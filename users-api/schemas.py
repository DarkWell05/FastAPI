from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str
    email: str
    age: int = Field(ge=0, le=150)


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = Field(default=None, ge=0, le=150)


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    age: int
    model_config = ConfigDict(from_attributes=True)
