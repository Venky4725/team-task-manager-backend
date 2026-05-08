from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    deadline: Optional[date] = None
    project_id: int
    assigned_to: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[date] = None
    assigned_to: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
