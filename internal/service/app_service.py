from dataclasses import dataclass
from uuid import uuid4, UUID

from injector import inject

from internal.model import App
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class AppService:
    db: SQLAlchemy

    def create_app(self) -> App:
        with self.db.auto_commit():
            app = App(
                account_id=uuid4(), name="AI应用", icon="icon", description="AI应用描述"
            )
            self.db.session.add(app)
        return app

    def get_app(self, id: UUID) -> App:
        app = self.db.session.query(App).get(id)
        return app

    def update_app(self, id: UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id)
            app.name = "修改后的名字"
        return app

    def delete_app(self, id: UUID):
        with self.db.auto_commit():
            app = self.get_app(id)
            self.db.session.delete(app)
        return app
