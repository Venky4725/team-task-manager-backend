from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.dashboard_service import DashboardService
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard statistics"""
    return DashboardService.get_stats(db, current_user)

@router.get("/recent-tasks")
def get_recent_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recent tasks"""
    return DashboardService.get_recent_tasks(db, current_user)
