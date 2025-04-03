from flask import Flask
from flask_migrate import Migrate

from internal.exception import CustomException
from internal.model import App
from internal.router import Router
from config import Config
from pkg.response import json, Response, HttpCode
from pkg.sqlalchemy import SQLAlchemy


class Http(Flask):
    """Http服务引擎"""

    def __init__(
            self,
            *args,
            router: Router,
            config: Config,
            db: SQLAlchemy,
            migrate: Migrate,
            **kwargs,
    ):
        # 1.调用父类构造函数初始化
        super().__init__(*args, **kwargs)
        # 5.注册应用路由
        router.register_router(self)
        self.config.from_object(config)
        self.register_error_handler(Exception, self._error_handler)
        db.init_app(self)
        migrate.init_app(self, db, directory="internal/migration")

    @staticmethod
    def _error_handler(error: Exception):
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {}
            ))
        return json(Response(code=HttpCode.FAIL, message=str(error), data={}))
