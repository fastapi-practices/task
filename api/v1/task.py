from typing import Annotated

from fastapi import APIRouter, Depends, Path
from taskiq import TaskiqResult

from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.plugin.task.schema.task import TaskSubmitSchema
from backend.plugin.task.service.task_service import TaskService

router = APIRouter()


@router.get('', summary='获取任务列表', dependencies=[DependsJwtAuth])
async def get_taskiq_tasks() -> ResponseModel:
    data = TaskService.get_available_tasks()
    return response_base.success(data=data)


@router.get('/{task_id}', summary='获取 Taskiq 任务结果', dependencies=[DependsJwtAuth])
async def get_taskiq_result(task_id: Annotated[str, Path(description='任务 ID')]) -> ResponseSchemaModel[TaskiqResult]:
    data = await TaskService.get_task_result(task_id=task_id)
    return response_base.success(data=data)


@router.post(
    '/execute',
    summary='执行任务',
    dependencies=[
        Depends(RequestPermission('sys:task:exec')),
        DependsRBAC,
    ],
)
async def execute_taskiq_task(obj: TaskSubmitSchema) -> ResponseModel:
    data = await TaskService.execute_task(task_name=obj.task_name, args=obj.args, kwargs=obj.kwargs, labels=obj.labels)
    return response_base.success(data=data)
