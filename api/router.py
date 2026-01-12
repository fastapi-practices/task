from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.task.api.v1.task import router as task_router

v1 = APIRouter(prefix=settings.FASTAPI_API_V1_PATH, tags=['Taskiq 任务'])

v1.include_router(task_router, prefix='/taskiq-tasks')
