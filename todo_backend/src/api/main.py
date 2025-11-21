from typing import Generator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import SessionLocal, engine, Base

# Create tables on startup to ensure database is ready
def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    """Dependency that provides a SQLAlchemy session and ensures proper cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="ToDo Backend API",
    description="FastAPI backend for a ToDo app with SQLite persistence.",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Health check endpoints"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this from env and restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """FastAPI startup event to initialize database and any other resources."""
    init_db()

@app.get("/", tags=["health"], summary="Health Check", description="Simple health-check endpoint.")
def health_check():
    """Return a simple health status payload."""
    return {"message": "Healthy"}
