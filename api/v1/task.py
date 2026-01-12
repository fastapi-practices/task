from typing import Annotated

from fastapi import APIRouter, Path

from backend.common.response.response_schema import ResponseModel, response_base
from backend.plugin.task.schema.task import TaskSubmitSchema
from backend.plugin.task.service.task_service import TaskService

router = APIRouter()


@router.get('', summary='获取任务列表')
async def get_taskiq_tasks() -> ResponseModel:
    data = TaskService.get_available_tasks()
    return response_base.success(data=data)


@router.get('/{task_id}/status', summary='查询 Taskiq 任务状态')
async def get_taskiq_status(task_id: Annotated[str, Path(description='任务 ID')]) -> ResponseModel:
    data = await TaskService.get_task_status(task_id=task_id)
    return response_base.success(data=data)


@router.get('/{task_id}', summary='获取 Taskiq 任务结果')
async def get_taskiq_result(task_id: Annotated[str, Path(description='任务 ID')]) -> ResponseModel:
    result = await TaskService.get_task_result(task_id=task_id)
    return response_base.success(
        data={
            'task_id': task_id,
            'result': result.return_value if not result.is_err else None,
            'error': str(result.error) if result.is_err else None,
        }
    )


@router.post('/execute', summary='执行任务')
async def execute_taskiq_task(obj: TaskSubmitSchema) -> ResponseModel:
    data = await TaskService.execute_task(task_name=obj.task_name, args=obj.args, kwargs=obj.kwargs, labels=obj.labels)
    return response_base.success(data=data)
