from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


# SQLAlchemy 类的扩展
class SQLAlchemy(_SQLAlchemy):
    # 使用上下文管理器自动提交事务
    @contextmanager
    def auto_commit(self):
        try:
            # 执行上下文中的代码
            yield
            # 如果没有异常发生，则提交事务
            self.session.commit()
        except Exception as e:
            # 如果发生异常，则回滚事务
            self.session.rollback()
            # 重新抛出异常
            raise e
