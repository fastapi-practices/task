import sys
import urllib.parse

from pathlib import Path

from taskiq import AsyncBroker, PrometheusMiddleware, TaskiqMiddleware
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from backend.core.conf import settings
from backend.plugin.task.tasks.base import TaskBaseMiddleware


def _is_taskiq_worker_process() -> bool:
    """判断当前进程是否由 taskiq worker 启动"""
    argv = [Path(arg).name for arg in sys.argv]
    if not argv:
        return False
    return 'taskiq' in argv[0] and 'worker' in argv[1:]


def get_broker() -> AsyncBroker:
    """获取 Taskiq Broker 实例"""
    broker_type = getattr(settings, 'TASKIQ_BROKER', settings.CELERY_BROKER)

    rabbitmq_url = f'amqp://{settings.CELERY_RABBITMQ_USERNAME}:{urllib.parse.quote(settings.CELERY_RABBITMQ_PASSWORD)}@{settings.CELERY_RABBITMQ_HOST}:{settings.CELERY_RABBITMQ_PORT}/{settings.CELERY_RABBITMQ_VHOST}'
    redis_url = f'redis://:{urllib.parse.quote(settings.REDIS_PASSWORD)}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.CELERY_BROKER_REDIS_DATABASE}'
    result_backend = RedisAsyncResultBackend(redis_url, prefix_str='fba_taskiq')

    broker = AioPikaBroker(rabbitmq_url).with_result_backend(result_backend)
    if broker_type == 'redis':
        broker = ListQueueBroker(redis_url).with_result_backend(result_backend)

    return broker


def get_middlewares() -> tuple[TaskiqMiddleware, ...]:
    """获取 Taskiq 中间件"""
    middlewares: list[TaskiqMiddleware] = [TaskBaseMiddleware()]

    if settings.GRAFANA_METRICS_ENABLE and _is_taskiq_worker_process():
        middlewares.append(
            PrometheusMiddleware(
                server_addr=settings.GRAFANA_TASKIQ_PROMETHEUS_SERVER_ADDR,
                server_port=settings.GRAFANA_TASKIQ_PROMETHEUS_SERVER_PORT,
            )
        )

    return tuple(middlewares)


# 创建 Taskiq broker 单例
taskiq_broker = get_broker().with_middlewares(*get_middlewares())
