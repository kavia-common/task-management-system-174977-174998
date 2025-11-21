import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL is configurable via environment variable; defaults to local SQLite file todos.db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todos.db")

# For SQLite, we need check_same_thread=False to allow usage across different threads in FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarative class
Base = declarative_base()
