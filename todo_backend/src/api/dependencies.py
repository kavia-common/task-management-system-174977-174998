from typing import Generator

from sqlalchemy.orm import Session

from .db import SessionLocal


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """Provide a database session for request handlers, ensuring proper cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
