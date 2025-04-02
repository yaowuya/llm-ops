import dotenv
from dotenv import load_dotenv
from injector import Injector

from config import Config
from internal.router import Router
from internal.server.http import Http

# 将env加载到环境变量中
dotenv.load_dotenv()

injector = Injector()

app = Http(
    __name__,
    router=injector.get(Router),
    config=Config()
)

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
