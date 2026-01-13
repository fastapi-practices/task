# 任务插件

基于 [taskiq](https://github.com/taskiq-python/taskiq) 的异步任务队列

## 配置

插件自动读取项目配置，优先使用 `TASKIQ_BROKER`，否则使用 `CELERY_BROKER`：

```python
# Redis
TASKIQ_BROKER = 'redis'  # 或 CELERY_BROKER
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
CELERY_BROKER_REDIS_DATABASE = 0

# RabbitMQ
TASKIQ_BROKER = 'rabbitmq'  # 或 CELERY_BROKER
CELERY_RABBITMQ_HOST = 'localhost'
CELERY_RABBITMQ_PORT = 5672
CELERY_RABBITMQ_USERNAME = 'guest'
CELERY_RABBITMQ_PASSWORD = 'guest'
CELERY_RABBITMQ_VHOST = '/'
```

## 快速开始

### 1. 集成生命周期

在 `backend/core/registrar.py` 的 `register_init` 函数中添加：

```python
from backend.plugin.task.broker import taskiq_broker


async def register_init(app):
    if not taskiq_broker.is_worker_process:
        await taskiq_broker.startup()
    yield
    if not taskiq_broker.is_worker_process:
        await taskiq_broker.shutdown()
```

### 2. 启动 Worker

```bash
taskiq worker backend.plugin.task.broker:taskiq_broker -d backend.plugin.task
```

## 定时任务

### 启动定时任务调度器（可选）

```bash
taskiq scheduler backend.plugin.task.scheduler:taskiq_scheduler -d backend.plugin.task.tasks.beat
```

在 `backend/plugin/task/tasks/beat.py` 中定义定时任务：

```python
@taskiq_broker.task(task_name='my_task', schedule=[{'cron': '*/5 * * * *'}])
async def my_task() -> str:
    return 'done'
```
