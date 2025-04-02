import os
from dataclasses import dataclass

from flask import request
from injector import inject
from openai import OpenAI


@inject
@dataclass
class AppHandler:
    """应用控制器"""

    def ping(self):
        return {"ping": "pong"}

    def completion(self):
        """聊天接口"""
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
        return content
