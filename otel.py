from taskiq.instrumentation import TaskiqInstrumentor

from backend.core.conf import settings

_taskiq_otel_instrumented = False


def init_taskiq_tracing() -> None:
    """
    初始化 Taskiq OpenTelemetry

    :return:
    """
    global _taskiq_otel_instrumented

    if not settings.GRAFANA_METRICS_ENABLE or _taskiq_otel_instrumented:
        return

    TaskiqInstrumentor().instrument()
    _taskiq_otel_instrumented = True
