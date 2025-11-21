from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Index
from .db import Base

class Todo(Base):
    """SQLAlchemy ORM model representing a to-do item."""

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_todos_completed_title", "completed", "title"),
    )
