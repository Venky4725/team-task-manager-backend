from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.post("", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new task"""
    return TaskService.create_task(db, task, current_user)

@router.get("", response_model=List[TaskResponse])
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    project_id: Optional[str] = Query(None),  # Changed to str to accept empty string
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tasks"""
    # Convert empty strings and string numbers to proper types
    project_id_int = None
    if project_id and project_id.strip():
        try:
            project_id_int = int(project_id)
        except ValueError:
            pass
    
    # Convert empty strings to None
    status_val = None if not status or status == "" else status
    priority_val = None if not priority or priority == "" else priority
    search_val = None if not search or search == "" else search
    
    return TaskService.get_tasks(db, current_user, skip, limit, project_id_int, status_val, priority_val, search_val)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single task"""
    return TaskService.get_task(db, task_id, current_user)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a task"""
    return TaskService.update_task(db, task_id, task, current_user)

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a task"""
    TaskService.delete_task(db, task_id, current_user)
    return {"message": "Task deleted successfully"}
