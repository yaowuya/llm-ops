from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ToolParamType(str, Enum):
    """工具类参数类型枚举类"""

    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    SELECT = "select"


class ToolParam(BaseModel):
    """工具类参数类型"""

    name: str
    label: str
    type: ToolParamType  # 参数类型
    required: bool = False  # 是否必填
    default: Optional[Any] = None  # 默认值
    min: Optional[float] = None  # 最小值
    max: Optional[float] = None  # 最大值
    options: list[dict[str, Any]] = Field(default_factory=list)  # 下拉菜单选项列表


class ToolEntity(BaseModel):
    """工具实体类，存储的信息映射的是工具名.yaml里的数据"""

    name: str  # 工具名称
    label: str  # 工具标签
    description: str  # 工具描述
    params: list[ToolParam] = Field(default_factory=list)  # 工具参数列表
