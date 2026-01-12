from typing import Any

from pydantic import Field

from backend.common.schema import SchemaBase


class TaskSubmitSchema(SchemaBase):
    """任务提交参数"""

    task_name: str = Field(..., description='任务名称')
    args: list[Any] = Field(default_factory=list, description='位置参数')
    kwargs: dict[str, Any] = Field(default_factory=dict, description='关键字参数')
    labels: dict[str, Any] = Field(default_factory=dict, description='任务标签')


class TaskStatusSchema(SchemaBase):
    """任务状态"""

    task_id: str = Field(..., description='任务 ID')
    is_ready: bool = Field(..., description='是否完成')
    is_error: bool = Field(..., description='是否出错')
    result: Any | None = Field(None, description='任务结果')
    error: str | None = Field(None, description='错误信息')
