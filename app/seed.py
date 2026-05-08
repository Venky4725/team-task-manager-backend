from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, engine
from app.database.base import Base

# Import all models to register them with SQLAlchemy
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.task import Task, TaskStatus, TaskPriority

from app.utils.security import hash_password
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    """Seed the database with demo data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_user = db.query(User).first()
        if existing_user:
            logger.info("Database already seeded. Skipping...")
            return
        
        logger.info("Seeding database...")
        
        # Create admin user
        admin = User(
            name="Admin User",
            email="admin@example.com",
            password_hash=hash_password("password123"),
            role=UserRole.ADMIN
        )
        db.add(admin)
        
        # Create member users
        member1 = User(
            name="John Doe",
            email="john@example.com",
            password_hash=hash_password("password123"),
            role=UserRole.MEMBER
        )
        db.add(member1)
        
        member2 = User(
            name="Jane Smith",
            email="jane@example.com",
            password_hash=hash_password("password123"),
            role=UserRole.MEMBER
        )
        db.add(member2)
        
        db.commit()
        db.refresh(admin)
        db.refresh(member1)
        db.refresh(member2)
        
        logger.info("Users created")
        
        # Create projects
        project1 = Project(
            name="Website Redesign",
            description="Redesign the company website with modern UI/UX",
            created_by=admin.id
        )
        db.add(project1)
        
        project2 = Project(
            name="Mobile App Development",
            description="Develop a mobile app for iOS and Android",
            created_by=admin.id
        )
        db.add(project2)
        
        db.commit()
        db.refresh(project1)
        db.refresh(project2)
        
        logger.info("Projects created")
        
        # Add project members
        members = [
            ProjectMember(project_id=project1.id, user_id=admin.id),
            ProjectMember(project_id=project1.id, user_id=member1.id),
            ProjectMember(project_id=project2.id, user_id=admin.id),
            ProjectMember(project_id=project2.id, user_id=member2.id),
        ]
        
        for member in members:
            db.add(member)
        
        db.commit()
        logger.info("Project members added")
        
        # Create tasks
        tasks = [
            Task(
                title="Design homepage mockup",
                description="Create a modern homepage design in Figma",
                status=TaskStatus.COMPLETED,
                priority=TaskPriority.HIGH,
                deadline=(datetime.now() - timedelta(days=2)).date(),
                project_id=project1.id,
                assigned_to=member1.id,
                created_by=admin.id
            ),
            Task(
                title="Implement responsive navigation",
                description="Build a responsive navigation menu with mobile support",
                status=TaskStatus.IN_PROGRESS,
                priority=TaskPriority.HIGH,
                deadline=(datetime.now() + timedelta(days=5)).date(),
                project_id=project1.id,
                assigned_to=member1.id,
                created_by=admin.id
            ),
            Task(
                title="Setup project repository",
                description="Initialize Git repository and setup CI/CD pipeline",
                status=TaskStatus.TODO,
                priority=TaskPriority.MEDIUM,
                deadline=(datetime.now() + timedelta(days=3)).date(),
                project_id=project1.id,
                assigned_to=member1.id,
                created_by=admin.id
            ),
            Task(
                title="Design app wireframes",
                description="Create wireframes for all app screens",
                status=TaskStatus.COMPLETED,
                priority=TaskPriority.HIGH,
                deadline=(datetime.now() - timedelta(days=5)).date(),
                project_id=project2.id,
                assigned_to=member2.id,
                created_by=admin.id
            ),
            Task(
                title="Setup React Native project",
                description="Initialize React Native project with required dependencies",
                status=TaskStatus.IN_PROGRESS,
                priority=TaskPriority.HIGH,
                deadline=(datetime.now() + timedelta(days=2)).date(),
                project_id=project2.id,
                assigned_to=member2.id,
                created_by=admin.id
            ),
            Task(
                title="Implement authentication flow",
                description="Build login and registration screens with API integration",
                status=TaskStatus.TODO,
                priority=TaskPriority.HIGH,
                deadline=(datetime.now() + timedelta(days=7)).date(),
                project_id=project2.id,
                assigned_to=member2.id,
                created_by=admin.id
            ),
            Task(
                title="Write API documentation",
                description="Document all API endpoints with examples",
                status=TaskStatus.TODO,
                priority=TaskPriority.LOW,
                deadline=(datetime.now() + timedelta(days=10)).date(),
                project_id=project2.id,
                assigned_to=None,
                created_by=admin.id
            ),
        ]
        
        for task in tasks:
            db.add(task)
        
        db.commit()
        logger.info("Tasks created")
        
        logger.info("Database seeded successfully!")
        logger.info("\nDemo Accounts:")
        logger.info("Admin: admin@example.com / password123")
        logger.info("Member 1: john@example.com / password123")
        logger.info("Member 2: jane@example.com / password123")
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Seed data
    seed_database()
