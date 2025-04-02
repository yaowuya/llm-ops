from flask import Flask

from internal.router import Router
from config import Config


class Http(Flask):
    """Http服务引擎"""

    def __init__(
            self,
            *args,
            router: Router,
            config: Config,
            **kwargs,
    ):
        # 1.调用父类构造函数初始化
        super().__init__(*args, **kwargs)
        # 5.注册应用路由
        router.register_router(self)
        self.config.from_object(config)
