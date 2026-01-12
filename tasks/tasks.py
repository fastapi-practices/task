from time import sleep

from anyio import sleep as asleep

from backend.plugin.task.broker import taskiq_broker


@taskiq_broker.task(task_name='taskiq_demo')
def taskiq_demo() -> str:
    """示例任务，模拟耗时操作"""
    sleep(30)
    return 'test async'


@taskiq_broker.task(task_name='taskiq_demo_async')
async def taskiq_demo_async() -> str:
    """异步示例任务，模拟耗时操作"""
    await asleep(30)
    return 'test async'


@taskiq_broker.task(task_name='taskiq_demo_params')
async def taskiq_demo_params(hello: str, world: str | None = None) -> str:
    """参数示例任务，模拟传参操作"""
    await asleep(1)
    return hello + (world or '')
