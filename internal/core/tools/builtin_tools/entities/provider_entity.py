from pydantic import BaseModel


class ProviderEntity(BaseModel):
    """服务提供商实体，映射的数据是providers.yaml里的每条记录"""

    name: str  # 服务提供商名称
    label: str  # 服务提供商标签
    description: str  # 服务提供商描述
    icon: str  # 图标地址
    background: str  # 图标的颜色
    category: str  # 分类信息
    created_at: int = 0  # 提供商/工具的创建时间戳


class Provider(BaseModel):
    """服务提供商，在该类下，可以获取到该服务提供商的所有工具、描述、图标等多个信息"""

    name: str  # 服务提供商名称
    position: int  # 服务提供商的顺序
    provider_entity: ProviderEntity  # 服务提供商实体
