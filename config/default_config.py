# 默认配置字典，包含应用程序的默认设置
DEFAULT_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": "",  # 数据库URI
    "SQLALCHEMY_ECHO": "True",  # SQLAlchemy回显设置
    "SQLALCHEMY_POOL_RECYCLE": "3600",  # SQLAlchemy连接池回收时间（秒）
    "SQLALCHEMY_POOL_SIZE": "30",  # SQLAlchemy连接池大小
    "WTF_CSRF_ENABLED": "False",  # CSRF保护设置
}
