"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    """Base book schema with common fields."""

    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=1000)
    price: float = Field(..., gt=0)


class BookCreate(BookBase):
    """Schema for creating a new book."""

    pass


class BookUpdate(BaseModel):
    """Schema for updating a book."""

    title: str | None = Field(None, min_length=1, max_length=255)
    author: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, min_length=1, max_length=1000)
    price: float | None = Field(None, gt=0)


class BookRead(BookBase):
    """Schema for reading a book."""

    id: int

    model_config = ConfigDict(from_attributes=True)
