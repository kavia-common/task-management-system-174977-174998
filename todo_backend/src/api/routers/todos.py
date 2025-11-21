from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import Todo as TodoModel
from ..schemas import TodoCreate, TodoRead, TodoUpdate

router = APIRouter(
    prefix="/api/todos",
    tags=["todos"],
)


def _get_todo_or_404(db: Session, todo_id: int) -> TodoModel:
    """Internal helper to fetch a Todo or raise 404."""
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id={todo_id} not found",
        )
    return todo


@router.get(
    "",
    response_model=List[TodoRead],
    summary="List ToDos",
    description="Retrieve all to-do items, ordered by creation time ascending.",
    responses={
        200: {"description": "List of to-do items"},
    },
)
def list_todos(db: Session = Depends(get_db)) -> List[TodoRead]:
    """Return all to-do items."""
    todos = db.query(TodoModel).order_by(TodoModel.created_at.asc()).all()
    return todos


@router.post(
    "",
    response_model=TodoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create ToDo",
    description="Create a new to-do item using the provided fields.",
    responses={
        201: {"description": "To-do created successfully"},
        422: {"description": "Validation error"},
    },
)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)) -> TodoRead:
    """Create a new to-do item."""
    todo = TodoModel(
        title=payload.title,
        description=payload.description,
        completed=bool(payload.completed) if payload.completed is not None else False,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.get(
    "/{id}",
    response_model=TodoRead,
    summary="Get ToDo by ID",
    description="Retrieve a single to-do item by its unique identifier.",
    responses={
        200: {"description": "The requested to-do item"},
        404: {"description": "To-do not found"},
    },
)
def get_todo_by_id(
    id: int = Path(..., description="ID of the to-do item", ge=1),
    db: Session = Depends(get_db),
) -> TodoRead:
    """Return a single to-do item by ID."""
    todo = _get_todo_or_404(db, id)
    return todo


@router.put(
    "/{id}",
    response_model=TodoRead,
    summary="Update ToDo",
    description="Update a to-do item. Fields not provided will remain unchanged.",
    responses={
        200: {"description": "Updated to-do item"},
        404: {"description": "To-do not found"},
    },
)
def update_todo(
    payload: TodoUpdate,
    id: int = Path(..., description="ID of the to-do item", ge=1),
    db: Session = Depends(get_db),
) -> TodoRead:
    """Update a to-do item with the provided fields."""
    todo = _get_todo_or_404(db, id)

    if payload.title is not None:
        todo.title = payload.title
    if payload.description is not None:
        todo.description = payload.description
    if payload.completed is not None:
        todo.completed = payload.completed

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.patch(
    "/{id}/toggle",
    response_model=TodoRead,
    summary="Toggle completion",
    description="Toggle the 'completed' status of the to-do item identified by ID.",
    responses={
        200: {"description": "Toggled to-do item"},
        404: {"description": "To-do not found"},
    },
)
def toggle_todo(
    id: int = Path(..., description="ID of the to-do item", ge=1),
    db: Session = Depends(get_db),
) -> TodoRead:
    """Toggle the completion status of a to-do item."""
    todo = _get_todo_or_404(db, id)
    todo.completed = not todo.completed
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete ToDo",
    description="Delete a to-do item by its ID.",
    responses={
        204: {"description": "Deletion successful (no content)"},
        404: {"description": "To-do not found"},
    },
)
def delete_todo(
    id: int = Path(..., description="ID of the to-do item", ge=1),
    db: Session = Depends(get_db),
) -> None:
    """Delete a to-do item by ID."""
    todo = _get_todo_or_404(db, id)
    db.delete(todo)
    db.commit()
    return None
