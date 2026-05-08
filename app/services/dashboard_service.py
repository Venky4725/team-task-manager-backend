from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models.task import Task, TaskStatus
from app.models.project import Project
from app.models.user import User, UserRole
from app.models.project_member import ProjectMember

class DashboardService:
    @staticmethod
    def get_stats(db: Session, user: User) -> dict:
        """Get dashboard statistics"""
        # Get accessible projects
        if user.role == UserRole.ADMIN:
            projects_query = db.query(Project)
            tasks_query = db.query(Task)
        else:
            accessible_projects = db.query(ProjectMember.project_id).filter(
                ProjectMember.user_id == user.id
            ).subquery()
            projects_query = db.query(Project).filter(Project.id.in_(accessible_projects))
            tasks_query = db.query(Task).filter(Task.project_id.in_(accessible_projects))
        
        # Count projects
        total_projects = projects_query.count()
        
        # Count tasks by status
        total_tasks = tasks_query.count()
        completed_tasks = tasks_query.filter(Task.status == TaskStatus.COMPLETED).count()
        pending_tasks = tasks_query.filter(Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])).count()
        
        # Count overdue tasks
        overdue_tasks = tasks_query.filter(
            Task.deadline < date.today(),
            Task.status != TaskStatus.COMPLETED
        ).count()
        
        # Calculate completion percentage
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "overdue_tasks": overdue_tasks,
            "completion_percentage": round(completion_percentage, 2)
        }
    
    @staticmethod
    def get_recent_tasks(db: Session, user: User, limit: int = 10):
        """Get recent tasks"""
        if user.role == UserRole.ADMIN:
            tasks_query = db.query(Task)
        else:
            accessible_projects = db.query(ProjectMember.project_id).filter(
                ProjectMember.user_id == user.id
            ).subquery()
            tasks_query = db.query(Task).filter(Task.project_id.in_(accessible_projects))
        
        return tasks_query.order_by(Task.created_at.desc()).limit(limit).all()
