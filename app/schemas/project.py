from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectMemberResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class ProjectResponse(ProjectBase):
    id: int
    created_by: int
    created_at: datetime
    members: List[ProjectMemberResponse] = []

    class Config:
        from_attributes = True

class AddMemberRequest(BaseModel):
    user_id: int
