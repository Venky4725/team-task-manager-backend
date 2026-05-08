from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here to ensure they are registered with SQLAlchemy
def import_models():
    from app.models import user, project, project_member, task
    return user, project, project_member, task
