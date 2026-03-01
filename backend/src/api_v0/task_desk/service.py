from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v0.common.errors import ItemNotFoundError
from src.api_v0.common.service import BaseRepo
from src.config import settings
from src.api_v0.task_desk.schemas import TaskModelSchema, TaskCreateSchema, TaskUpdateSchema
from src.database.models import Task, TaskCategory
import logging

logger = logging.getLogger(__name__)


class TaskService(BaseRepo[Task, TaskModelSchema]):
    def __init__(self):
        super().__init__(Task, TaskModelSchema)

    def create_task(self, task_data: TaskCreateSchema, session: AsyncSession):
        pass