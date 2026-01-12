from anyio import sleep as asleep

from backend.plugin.task.broker import taskiq_broker


@taskiq_broker.task(task_name='scheduled_demo', schedule=[{'cron': '*/30 * * * *'}])
async def scheduled_demo() -> str:
    """定时同步任务，每30秒执行一次"""
    await asleep(0.001)
    return 'scheduled demo'


@taskiq_broker.task(task_name='scheduled_demo_async', schedule=[{'cron': '*/1 * * * *'}])
async def scheduled_demo_async() -> str:
    """定时异步任务，每分钟执行一次"""
    await asleep(0.001)
    return 'scheduled demo async'


@taskiq_broker.task(
    task_name='scheduled_demo_params',
    schedule=[{'cron': '*/1 * * * *', 'args': ['你好，'], 'kwargs': {'world': '世界'}}],
)
async def scheduled_demo_params(hello: str, world: str | None = None) -> str:
    """定时参数任务，每分钟执行一次"""
    await asleep(0.001)
    return hello + (world or '')
