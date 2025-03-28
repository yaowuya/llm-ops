from dataclasses import dataclass

from injector import inject


@inject
@dataclass
class AppHandler:
    """应用控制器"""

    def ping(self):
        return {"ping": "pong"}
