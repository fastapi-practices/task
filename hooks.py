from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.plugin.task.broker import taskiq_broker
from backend.plugin.task.otel import init_taskiq_tracing


def otel(_app: FastAPI) -> None:
    """Taskiq OpenTelemetry"""
    init_taskiq_tracing()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    """Taskiq broker 生命周期"""
    if not taskiq_broker.is_worker_process:
        await taskiq_broker.startup()

    try:
        yield
    finally:
        if not taskiq_broker.is_worker_process:
            await taskiq_broker.shutdown()
