from typing import Any

from taskiq import TaskiqResult

from backend.common.exception import errors
from backend.plugin.task.broker import taskiq_broker
from backend.plugin.task.schema.task import TaskStatusSchema


class TaskService:
    """任务队列服务类"""

    @staticmethod
    def get_available_tasks() -> list[str]:
        """获取可用任务列表"""
        return sorted(taskiq_broker.get_all_tasks().keys())

    @staticmethod
    async def get_task_status(task_id: str) -> TaskStatusSchema:
        """
        获取任务状态

        :param task_id: 任务 ID
        :return:
        """
        result = await taskiq_broker.result_backend.get_result(task_id)
        if result is None:
            raise errors.NotFoundError(msg=f'任务 {task_id} 不存在或结果已过期')
        return TaskStatusSchema(
            task_id=task_id,
            is_ready=result.is_ready,
            is_error=result.is_err,
            result=result.return_value if result.is_ready and not result.is_err else None,
            error=str(result.error) if result.is_err else None,
        )

    @staticmethod
    async def get_task_result(task_id: str) -> TaskiqResult:
        """
        获取任务结果

        :param task_id: 任务 ID
        :return:
        """
        result = await taskiq_broker.result_backend.get_result(task_id)
        if result is None:
            raise errors.NotFoundError(msg=f'任务 {task_id} 不存在或结果已过期')
        if not result.is_ready:
            raise errors.ForbiddenError(msg=f'任务 {task_id} 尚未完成')
        return result

    @staticmethod
    async def execute_task(task_name: str, args: list[Any], kwargs: dict[str, Any], labels: dict[str, Any]) -> str:
        """
        执行任务

        :param task_name: 任务名称
        :param args: 位置参数
        :param kwargs: 关键字参数
        :param labels: 任务标签
        :return:
        """
        task_func = taskiq_broker.find_task(task_name)
        if not task_func:
            raise errors.NotFoundError(msg=f'任务 {task_name} 不存在')
        task = await task_func.kiq(*args, **kwargs, labels=labels)
        return task.task_id
