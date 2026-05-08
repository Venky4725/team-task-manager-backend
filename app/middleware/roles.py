from fastapi import HTTPException, status
from app.models.user import User, UserRole

def require_admin(current_user: User):
    """Require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def check_project_access(user: User, project_id: int, db) -> bool:
    """Check if user has access to a project"""
    from app.models.project_member import ProjectMember
    from app.models.project import Project
    
    # Admin has access to all projects
    if user.role == UserRole.ADMIN:
        return True
    
    # Check if user is project creator
    project = db.query(Project).filter(Project.id == project_id).first()
    if project and project.created_by == user.id:
        return True
    
    # Check if user is a member
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    ).first()
    
    return membership is not None
