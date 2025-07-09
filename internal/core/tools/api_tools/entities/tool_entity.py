from pydantic import BaseModel, Field


class ToolEntity(BaseModel):
    """API工具实体信息，记录了创建LangChain工具所需的配置信息"""

    id: str = Field(default="", description="API工具提供者对应的id")
    name: str = Field(default="", description="API工具名称")
    url: str = Field(default="", description="API工具请求的URL地址")
    method: str = Field(default="GET", description="API工具请求方法，默认为GET")
    description: str = Field(default="", description="API工具描述信息")
    headers: list[dict] = Field(default_factory=list, description="API工具请求头信息，格式为[{key: value}]")
    parameters: list[dict] = Field(default_factory=list, description="API工具请求参数，格式为[{key: value}]")
