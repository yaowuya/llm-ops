import os
from dataclasses import dataclass
from uuid import UUID

from flask import request
from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import OpenAI

from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import validate_error_json, success_json, success_message


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def ping(self):
        # return {"ping": "pong"}
        raise FailException(message="异常")

    def debug(self, app_id: UUID):
        """聊天接口"""
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)
        # 2.构建组件
        prompt = ChatPromptTemplate.from_template("{query}")
        llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
        parser = StrOutputParser()

        # 3.构建链
        chain = prompt | llm | parser
        # 4.调用链得到结果
        content = chain.invoke({"query": req.query.data})
        return success_json({"content": content})

    def create_app(self):
        """创建应用"""
        app = self.app_service.create_app()
        return success_message(f"创建应用成功,应用ID:{app.id}")

    def get_app(self, id: UUID):
        app = self.app_service.get_app(id)
        return success_message(f"获取应用成功, 应用名称: {app.name}")

    def update_app(self, id: UUID):
        app = self.app_service.update_app(id)
        return success_message(f"更新应用成功, 应用名称: {app.name}")

    def delete_app(self, id: UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"删除应用成功, 应用ID: {app.id}")
