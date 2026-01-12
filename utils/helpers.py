import asyncio

from typing import Any

from backend.plugin.task.broker import taskiq_broker


async def submit_and_wait(task_name: str, *args, timeout: float = 30.0, **kwargs) -> Any | None:
    """
    提交任务并等待结果

    :param task_name: 任务名称
    :param args: 位置参数
    :param timeout: 超时时间
    :param kwargs: 关键字参数
    :return:
    """
    try:
        task_func = taskiq_broker.find_task(task_name)
        if not task_func:
            return None

        task = await task_func.kiq(*args, **kwargs)
        result = await task.wait_result(timeout=timeout)

        if result.is_err:
            return None

    except asyncio.TimeoutError:
        return None
    except Exception:
        return None
    return result.return_value


async def batch_submit(task_name: str, items: list[dict], **common_kwargs) -> list[str]:
    """
    批量提交任务

    :param task_name: 任务名称
    :param items: 任务参数列表
    :param common_kwargs: 公共关键字参数
    :return:
    """
    task_ids = []

    try:
        task_func = taskiq_broker.find_task(task_name)
        if not task_func:
            return []

        for item in items:
            kwargs = {**common_kwargs, **item}
            task = await task_func.kiq(**kwargs)
            task_ids.append(task.task_id)

    except Exception:
        return task_ids
    return task_ids


async def wait_all(task_ids: list[str], timeout: float = 60.0) -> list[Any]:
    """
    等待所有任务完成

    :param task_ids: 任务 ID 列表
    :param timeout: 超时时间
    :return:
    """
    results = []

    try:
        for task_id in task_ids:
            result = await taskiq_broker.result_backend.get_result(task_id, timeout=timeout)
            if result and result.is_ready:
                if result.is_err:
                    results.append(None)
                else:
                    results.append(result.return_value)
            else:
                results.append(None)

    except Exception:
        return results
    return results


def get_task_info(task_name: str) -> dict | None:
    """
    获取任务信息

    :param task_name: 任务名称
    :return:
    """
    try:
        task_func = taskiq_broker.find_task(task_name)
        if not task_func:
            return None
    except Exception:
        return None

    return {
        'name': task_name,
        'function': task_func.__name__,
        'doc': task_func.__doc__,
        'module': task_func.__module__,
    }
