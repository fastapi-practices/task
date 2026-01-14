from typing import Any

from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult

from backend.common.socketio.actions import task_notification


class TaskBaseMiddleware(TaskiqMiddleware):
    """Taskiq 任务中间件"""

    async def pre_execute(self, message: 'TaskiqMessage') -> TaskiqMessage:
        """
        任务开始前执行

        :param message: 任务上下文
        :return:
        """
        await task_notification(msg=f'任务 {message.task_name}（{message.task_id}）开始执行')
        return message

    async def post_execute(self, message: 'TaskiqMessage', result: 'TaskiqResult[Any]') -> None:
        """
        任务成功后执行

        :param message: 任务上下文
        :param result: 任务返回值
        :return:
        """
        await task_notification(msg=f'任务 {message.task_name}（{message.task_id}）执行成功')

    async def on_error(self, message: 'TaskiqMessage', result: 'TaskiqResult[Any]', exception: BaseException) -> None:
        """
        任务失败后执行

        :param message: 任务上下文
        :param result: 任务返回值
        :param exception: 异常对象
        :return:
        """
        await task_notification(msg=f'任务 {message.task_name}（{message.task_id}）执行失败: {exception}')
