from injector import inject, singleton
from pydantic import BaseModel, Field

from internal.core.tools.builtin_tools.entities.provider_entity import Provider


@inject
@singleton
class BuiltinProviderManager(BaseModel):
    """服务提供商工厂类"""

    provider_map: dict[str, Provider] = Field(default_factory=dict)
