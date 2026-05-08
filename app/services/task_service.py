from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.task import Task, TaskStatus
from app.models.user import User, UserRole
from app.schemas.task import TaskCreate, TaskUpdate
from app.middleware.roles import check_project_access

class TaskService:
    @staticmethod
    def create_task(db: Session, task_data: TaskCreate, user: User) -> Task:
        """Create a new task"""
        # Check project access
        if not check_project_access(user, task_data.project_id, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )
        
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            deadline=task_data.deadline,
            project_id=task_data.project_id,
            assigned_to=task_data.assigned_to,
            created_by=user.id
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        return new_task
    
    @staticmethod
    def get_tasks(
        db: Session,
        user: User,
        skip: int = 0,
        limit: int = 100,
        project_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Task]:
        """Get all tasks accessible to the user"""
        query = db.query(Task)
        
        # Filter by project
        if project_id:
            if not check_project_access(user, project_id, db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to this project"
                )
            query = query.filter(Task.project_id == project_id)
        else:
            # If not admin, filter by user's projects
            if user.role != UserRole.ADMIN:
                from app.models.project_member import ProjectMember
                accessible_projects = db.query(ProjectMember.project_id).filter(
                    ProjectMember.user_id == user.id
                ).subquery()
                query = query.filter(Task.project_id.in_(accessible_projects))
        
        # Filter by status
        if status:
            query = query.filter(Task.status == status)
        
        # Filter by priority
        if priority:
            query = query.filter(Task.priority == priority)
        
        # Filter by search term
        if search:
            query = query.filter(Task.title.ilike(f"%{search}%"))
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_task(db: Session, task_id: int, user: User) -> Task:
        """Get a single task"""
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Check access
        if not check_project_access(user, task.project_id, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return task
    
    @staticmethod
    def update_task(db: Session, task_id: int, task_data: TaskUpdate, user: User) -> Task:
        """Update a task"""
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Check access
        if not check_project_access(user, task.project_id, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Members can only update status of their assigned tasks
        if user.role == UserRole.MEMBER:
            if task.assigned_to != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only update your assigned tasks"
                )
            # Members can only update status
            if task_data.status is not None:
                task.status = task_data.status
        else:
            # Admin can update all fields
            if task_data.title is not None:
                task.title = task_data.title
            if task_data.description is not None:
                task.description = task_data.description
            if task_data.status is not None:
                task.status = task_data.status
            if task_data.priority is not None:
                task.priority = task_data.priority
            if task_data.deadline is not None:
                task.deadline = task_data.deadline
            if task_data.assigned_to is not None:
                task.assigned_to = task_data.assigned_to
        
        db.commit()
        db.refresh(task)
        
        return task
    
    @staticmethod
    def delete_task(db: Session, task_id: int, user: User):
        """Delete a task"""
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Check access
        if not check_project_access(user, task.project_id, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Only admin can delete
        if user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin can delete tasks"
            )
        
        db.delete(task)
        db.commit()
