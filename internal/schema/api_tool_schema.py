from marshmallow import Schema, fields, pre_dump
from pydantic import BaseModel, Field, HttpUrl, field_validator
from wtforms import StringField
from wtforms.validators import Optional

from internal.model import ApiTool, ApiToolProvider
from pkg.paginator.paginator import PaginatorReq


class HeaderItem(BaseModel):
    """请求头项"""

    key: str
    value: str


class ValidateOpenAPISchemaReq(BaseModel):
    """校验OpenAPI规范请求"""

    openapi_schema: dict


class CreateApiToolReq(BaseModel):
    """创建自定义API工具请求"""

    name: str = Field(..., min_length=1, max_length=30, description="工具提供者名字")
    icon: HttpUrl = Field(..., description="工具提供者的图标URL")
    openapi_schema: dict = Field(..., description="OpenAPI规范的JSON对象")
    headers: list[HeaderItem] = Field(default=[], description="请求头列表")

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("工具提供者名字不能为空")
        return v.strip()


class UpdateApiToolProviderReq(BaseModel):
    """更新API工具提供者请求"""

    name: str = Field(..., min_length=1, max_length=30, description="工具提供者名字")
    icon: HttpUrl = Field(..., description="工具提供者的图标URL")
    openapi_schema: dict = Field(..., description="OpenAPI规范的JSON对象")
    headers: list[HeaderItem] = Field(default=[], description="请求头列表")

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("工具提供者名字不能为空")
        return v.strip()


class GetApiToolProvidersWithPageReq(PaginatorReq):
    """获取API工具提供者分页列表请求"""

    search_word = StringField("search_word", validators=[Optional()])


class GetApiToolProviderResp(Schema):
    """获取API工具提供者响应信息"""

    id = fields.UUID()
    name = fields.String()
    icon = fields.String()
    openapi_schema = fields.String()
    headers = fields.List(fields.Dict, default=[])
    created_at = fields.Integer(default=0)

    @pre_dump
    def process_data(self, data: ApiToolProvider, **kwargs):
        return {
            "id": data.id,
            "name": data.name,
            "icon": data.icon,
            "openapi_schema": data.openapi_schema,
            "headers": data.headers,
            "created_at": int(data.created_at.timestamp()),
        }


class GetApiToolResp(Schema):
    """获取API工具参数详情响应"""

    id = fields.UUID()
    name = fields.String()
    description = fields.String()
    inputs = fields.List(fields.Dict, default=[])
    provider = fields.Dict()

    @pre_dump
    def process_data(self, data: ApiTool, **kwargs):
        provider = data.provider
        return {
            "id": data.id,
            "name": data.name,
            "description": data.description,
            "inputs": [{k: v for k, v in parameter.items() if k != "in"} for parameter in data.parameters],
            "provider": {
                "id": provider.id,
                "name": provider.name,
                "icon": provider.icon,
                "description": provider.description,
                "headers": provider.headers,
            },
        }


class GetApiToolProvidersWithPageResp(Schema):
    """获取API工具提供者分页列表数据响应"""

    id = fields.UUID()
    name = fields.String()
    icon = fields.String()
    description = fields.String()
    headers = fields.List(fields.Dict, default=[])
    tools = fields.List(fields.Dict, default=[])
    created_at = fields.Integer(default=0)

    @pre_dump
    def process_data(self, data: ApiToolProvider, **kwargs):
        tools = data.tools
        return {
            "id": data.id,
            "name": data.name,
            "icon": data.icon,
            "description": data.description,
            "headers": data.headers,
            "tools": [
                {
                    "id": tool.id,
                    "description": tool.description,
                    "name": tool.name,
                    "inputs": [{k: v for k, v in parameter.items() if k != "in"} for parameter in tool.parameters],
                }
                for tool in tools
            ],
            "created_at": int(data.created_at.timestamp()),
        }
