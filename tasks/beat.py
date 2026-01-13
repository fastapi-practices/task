from time import sleep

from anyio import sleep as asleep

from backend.core.conf import settings
from backend.plugin.task.broker import taskiq_broker


@taskiq_broker.task(
    task_name='taskiq_schedule_demo', schedule=[{'interval': '30', 'cron_offset': settings.DATETIME_TIMEZONE}]
)
def scheduled_demo() -> str:
    """定时同步任务，每30秒执行一次"""
    sleep(0.001)
    return 'test sync'


@taskiq_broker.task(
    task_name='taskiq_schedule_demo_async',
    schedule=[{'cron': '*/1 * * * *', 'cron_offset': settings.DATETIME_TIMEZONE}],
)
async def scheduled_demo_async() -> str:
    """定时异步任务，每分钟执行一次"""
    await asleep(0.001)
    return 'test async'


@taskiq_broker.task(
    task_name='taskiq_schedule_demo_params',
    schedule=[
        {
            'cron': '*/1 * * * *',
            'cron_offset': settings.DATETIME_TIMEZONE,
            'args': ['你好，'],
            'kwargs': {'world': '世界'},
        }
    ],
)
async def scheduled_demo_params(hello: str, world: str | None = None) -> str:
    """定时参数任务，每分钟执行一次"""
    await asleep(0.001)
    return hello + (world or '')
