import os
from dataclasses import dataclass

from flask import request
from injector import inject
from openai import OpenAI

from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from pkg.response import validate_error_json, success_json


@inject
@dataclass
class AppHandler:
    """应用控制器"""

    def ping(self):
        # return {"ping": "pong"}
        raise FailException(message="异常")

    def completion(self):
        """聊天接口"""
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)
        query = request.json.get("query")
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个openai开发的聊天机器人,请根据用户的输入回复对应的信息"},
                {"role": "user", "content": query},
            ],
        )
        content = completion.choices[0].message.content
        return success_json({"content": content})
