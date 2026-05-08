from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, AddMemberRequest
from app.services.project_service import ProjectService
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.post("", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new project"""
    new_project = ProjectService.create_project(db, project, current_user.id)
    
    # Transform to include member details
    return {
        "id": new_project.id,
        "name": new_project.name,
        "description": new_project.description,
        "created_by": new_project.created_by,
        "created_at": new_project.created_at,
        "members": [
            {
                "id": member.user.id,
                "name": member.user.name,
                "email": member.user.email,
                "role": member.user.role.value
            }
            for member in new_project.members
        ]
    }

@router.get("", response_model=List[ProjectResponse])
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all projects"""
    # Convert empty string to None
    if search == "":
        search = None
    
    projects = ProjectService.get_projects(db, current_user, skip, limit, search)
    
    # Transform projects to include member details
    result = []
    for project in projects:
        project_dict = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_by": project.created_by,
            "created_at": project.created_at,
            "members": [
                {
                    "id": member.user.id,
                    "name": member.user.name,
                    "email": member.user.email,
                    "role": member.user.role.value
                }
                for member in project.members
            ]
        }
        result.append(project_dict)
    
    return result

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single project"""
    project = ProjectService.get_project(db, project_id, current_user)
    
    # Transform to include member details
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_by": project.created_by,
        "created_at": project.created_at,
        "members": [
            {
                "id": member.user.id,
                "name": member.user.name,
                "email": member.user.email,
                "role": member.user.role.value
            }
            for member in project.members
        ]
    }

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a project"""
    updated_project = ProjectService.update_project(db, project_id, project, current_user)
    
    # Transform to include member details
    return {
        "id": updated_project.id,
        "name": updated_project.name,
        "description": updated_project.description,
        "created_by": updated_project.created_by,
        "created_at": updated_project.created_at,
        "members": [
            {
                "id": member.user.id,
                "name": member.user.name,
                "email": member.user.email,
                "role": member.user.role.value
            }
            for member in updated_project.members
        ]
    }

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a project"""
    ProjectService.delete_project(db, project_id, current_user)
    return {"message": "Project deleted successfully"}

@router.post("/{project_id}/members")
def add_member(
    project_id: int,
    request: AddMemberRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a member to a project"""
    ProjectService.add_member(db, project_id, request.user_id, current_user)
    return {"message": "Member added successfully"}
