from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User, UserRole
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.middleware.roles import check_project_access

class ProjectService:
    @staticmethod
    def create_project(db: Session, project_data: ProjectCreate, user_id: int) -> Project:
        """Create a new project"""
        new_project = Project(
            name=project_data.name,
            description=project_data.description,
            created_by=user_id
        )
        
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        
        # Add creator as a member
        member = ProjectMember(project_id=new_project.id, user_id=user_id)
        db.add(member)
        db.commit()
        
        return new_project
    
    @staticmethod
    def get_projects(db: Session, user: User, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Project]:
        """Get all projects accessible to the user"""
        query = db.query(Project)
        
        # Filter by search term
        if search:
            query = query.filter(Project.name.ilike(f"%{search}%"))
        
        # If not admin, filter by user's projects
        if user.role != UserRole.ADMIN:
            query = query.join(ProjectMember).filter(ProjectMember.user_id == user.id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_project(db: Session, project_id: int, user: User) -> Project:
        """Get a single project"""
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Check access
        if not check_project_access(user, project_id, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return project
    
    @staticmethod
    def update_project(db: Session, project_id: int, project_data: ProjectUpdate, user: User) -> Project:
        """Update a project"""
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Only admin or creator can update
        if user.role != UserRole.ADMIN and project.created_by != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only project creator or admin can update"
            )
        
        # Update fields
        if project_data.name is not None:
            project.name = project_data.name
        if project_data.description is not None:
            project.description = project_data.description
        
        db.commit()
        db.refresh(project)
        
        return project
    
    @staticmethod
    def delete_project(db: Session, project_id: int, user: User):
        """Delete a project"""
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Only admin or creator can delete
        if user.role != UserRole.ADMIN and project.created_by != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only project creator or admin can delete"
            )
        
        db.delete(project)
        db.commit()
    
    @staticmethod
    def add_member(db: Session, project_id: int, user_id: int, current_user: User):
        """Add a member to a project"""
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Only admin or creator can add members
        if current_user.role != UserRole.ADMIN and project.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only project creator or admin can add members"
            )
        
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if already a member
        existing = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member"
            )
        
        # Add member
        member = ProjectMember(project_id=project_id, user_id=user_id)
        db.add(member)
        db.commit()
        
        return member
