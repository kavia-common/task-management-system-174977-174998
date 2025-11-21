from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import engine, Base
from .routers.todos import router as todos_router

# Create tables on startup to ensure database is ready
def init_db() -> None:
    """Initialize database tables by creating all metadata."""
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ToDo Backend API",
    description="FastAPI backend for a ToDo app with SQLite persistence.",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Health check endpoints"},
        {"name": "todos", "description": "To-do management endpoints"},
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

# Include routers
app.include_router(todos_router)
