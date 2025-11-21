from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class TodoBase(BaseModel):
    """Base fields shared by create and update schemas for a to-do item."""

    title: str = Field(..., description="Short title of the to-do item", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Detailed description of the to-do item")
    completed: Optional[bool] = Field(False, description="Whether the to-do item is marked as complete")


# PUBLIC_INTERFACE
class TodoCreate(TodoBase):
    """Schema for creating a new to-do item."""
    pass


# PUBLIC_INTERFACE
class TodoUpdate(BaseModel):
    """Schema for updating an existing to-do item (partial updates allowed)."""

    title: Optional[str] = Field(None, description="Short title of the to-do item", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Detailed description of the to-do item")
    completed: Optional[bool] = Field(None, description="Whether the to-do item is marked as complete")


# PUBLIC_INTERFACE
class TodoRead(BaseModel):
    """Schema for reading a to-do item as returned by the API."""

    id: int = Field(..., description="Unique identifier of the to-do item")
    title: str = Field(..., description="Short title of the to-do item")
    description: Optional[str] = Field(None, description="Detailed description of the to-do item")
    completed: bool = Field(..., description="Whether the to-do item is marked as complete")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")

    class Config:
        from_attributes = True  # Enables reading data from ORM objects
