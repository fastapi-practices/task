import urllib.parse

from typing import Literal

from taskiq import AsyncBroker
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from backend.core.conf import settings
from backend.plugin.task.tasks.base import TaskBaseMiddleware


def get_broker() -> AsyncBroker:
    """获取 Taskiq Broker 实例"""
    broker_type: Literal['redis', 'rabbitmq', 'memory'] = getattr(settings, 'TASKIQ_BROKER', settings.CELERY_BROKER)

    rabbitmq_url = f'amqp://{settings.CELERY_RABBITMQ_USERNAME}:{urllib.parse.quote(settings.CELERY_RABBITMQ_PASSWORD)}@{settings.CELERY_RABBITMQ_HOST}:{settings.CELERY_RABBITMQ_PORT}/{settings.CELERY_RABBITMQ_VHOST}'
    redis_url = f'redis://:{urllib.parse.quote(settings.REDIS_PASSWORD)}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.CELERY_BROKER_REDIS_DATABASE}'
    result_backend = RedisAsyncResultBackend(redis_url)
    broker = AioPikaBroker(rabbitmq_url).with_result_backend(result_backend)

    if broker_type == 'redis':
        broker = ListQueueBroker(redis_url).with_result_backend(result_backend)

    return broker


taskiq_broker = get_broker().with_middlewares(TaskBaseMiddleware())
