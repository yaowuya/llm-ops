import os
from typing import Any

from config.default_config import DEFAULT_CONFIG


def _get_env(key: str) -> Any:
    return os.getenv(key, DEFAULT_CONFIG.get(key))


def _get_bool_env(key: str) -> bool:
    value: str = _get_env(key)
    return value.lower() == "true" if value is not None else False


class Config:
    def __init__(self):
        # 从环境变量或默认配置加载CSRF保护设置
        self.WTF_CSRF_ENABLED = _get_bool_env("WTF_CSRF_ENABLED")
        # 从环境变量或默认配置加载数据库URI
        self.SQLALCHEMY_DATABASE_URI = _get_env("SQLALCHEMY_DATABASE_URI")
        # 从环境变量或默认配置加载SQLAlchemy引擎选项
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": int(_get_env("SQLALCHEMY_POOL_SIZE")),
            "pool_recycle": int(_get_env("SQLALCHEMY_POOL_RECYCLE")),
        }
        # 从环境变量或默认配置加载SQLAlchemy回显设置
        self.SQLALCHEMY_ECHO = _get_bool_env("SQLALCHEMY_ECHO")
