# Task

基于 [taskiq](https://github.com/taskiq-python/taskiq) 的异步任务队列插件，支持 Worker 和定时任务调度器

## 插件类型

- 应用级插件

## 配置说明

插件自动读取项目原始任务队列配置，优先使用 `TASKIQ_BROKER`，否则使用 `CELERY_BROKER`

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

## 使用方式

1. 安装并启用插件后，重启后端服务
2. 自 fba v1.13.3 起，插件安装后会自动应用；旧版本需手动将 `hooks.py` 中的 lifespan 添加到
   `backend/core/registrar.py::register_init` 中
3. 使用以下命令启动 Worker：

    ```bash
    taskiq worker backend.plugin.task.broker:taskiq_broker backend.plugin.task.tasks.beat -fsd -tp backend/plugin/task/**/tasks.py
    ```

4. 如需定时任务，使用以下命令启动调度器：

    ```bash
    taskiq scheduler backend.plugin.task.scheduler:taskiq_scheduler backend.plugin.task.tasks.beat
    ```

## 卸载说明

- 卸载插件前，先停止 Worker 和 Scheduler
- 卸载插件后，清理业务中的任务调用和队列配置

## 联系方式

- 作者：`wu-clan`
- 反馈方式：提交 Issue 或 PR
