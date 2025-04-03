import dotenv
from flask_migrate import Migrate
from injector import Injector

from app.http.module import ExtensionModule
from config import Config
from internal.router import Router
from internal.server.http import Http
from pkg.sqlalchemy import SQLAlchemy

# 将env加载到环境变量中
dotenv.load_dotenv()

injector = Injector([ExtensionModule])

app = Http(
    __name__,
    router=injector.get(Router),
    config=Config(),
    db=injector.get(SQLAlchemy),
    migrate=injector.get(Migrate),
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
