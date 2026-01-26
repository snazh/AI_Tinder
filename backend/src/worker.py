from src.tasks.celery_app import celery_app
import src.tasks.email_tasks
__all__ = ("celery_app",)
