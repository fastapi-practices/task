from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from backend.plugin.task.broker import taskiq_broker


def get_scheduler() -> TaskiqScheduler:
    """获取 Taskiq 调度器实例"""
    scheduler = TaskiqScheduler(
        broker=taskiq_broker,
        sources=[LabelScheduleSource(taskiq_broker)],
    )
    return scheduler


taskiq_scheduler = get_scheduler()
