# 启动

### 配置文件.env

在根目录下，创建.env文件，存储环境变量

```python
# Flask基础配置
FLASK_DEBUG=1
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=postgresql://postgres:root@localhost:5432/llm-ops
```

### pycharm启动

![](static/imgs/pycharm-start.png)

### 自动化生成requirements.txt

先安装pipres依赖

```
pip install --no-deps pipreqs
pip install yarg==0.1.9 docopt==0.6.2
```

pycharm配置

```python
pipreqs --ignore venv --force
```

![](static/imgs/pycharm-pipreqs.png)

# 项目说明

## 代码目录

```python
|---app // 应用入口集合
| ├---__init__.py
| └---http
|---config // 应用配置文件
| ├---__init__.py
| ├---config.py
| └---default_config.py
|---internal // 应用所有内部文件夹
| ├---core // LLM核心文件，集成LangChain、LLM、Embedding等非逻辑的代码
| | |---agent
| | |---chain
| | |---prompt
| | |---model_runtime
| | |---moderation
| | |---tool
| | |---vector_store
| | └---...
| ├---exception // 通用公共异常目录
| | ├---__init__.py
| | ├---exception.py
| | └---...
| ├---extension // Flask扩展文件目录
| | ├---__init__.py
| | ├---database_extension.py
| | └---...
| ├---handler // 路由处理器、控制器目录
| | ├---__init__.py
| | ├---account_handler.py
| | └---...
| ├---middleware // 应用中间件目录，包含校验是否登录
| | ├---__init__.py
| | └---middleware.py
| | └---...
| ├---migration // 数据库迁移文件目录，自动生成
| | ├---versions
| | └---...
| ├---model // 数据库模型文件目录
| | ├---__init__.py
| | ├---account.py
| | └---...
| ├---router // 应用路由文件夹
| | ├---__init__.py
| | ├---router.py
| | └---...
| ├---schedule // 调度任务、定时任务文件夹
| | ├---__init__.py
| | └---...
| ├---schema // 请求和响应的结构体
| | ├---__init__.py
| | └---...
| ├---server // 构建的应用，与app文件夹对应
| | ├---__init__.py
| | └---...
| ├---service // 服务层文件夹
| | ├---__init__.py
| | ├---oauth_service.py
| | └---...
| ├---task // 任务文件夹，支持即时任务+延迟任务
| | ├---__init__.py
| | └---...
|---pkg // 扩展包文件夹
| ├---__init__.py
| |---oauth
| | ├---__init__.py
| | ├---github_oauth.py
| | └---...
| └---... ├---storage // 本地存储文件夹
├---test // 测试目录
├---venv // 虚拟环境
├---.env // 应用配置文件
├---.gitignore // 配置git忽略文件
├---requirements.txt // 第三方包依赖管理
└---README.md // 项目说明文件
```

## pre-commit

安装pre-commit

```
pip install pre-commit
```

安装所有pre-commit钩子中声明的工具

```
pre-commit install
```

# 开发需要的网站

### 调试 LLM 应用程序的平台

https://smith.langchain.com/

### 向量数据库

https://console.weaviate.cloud/

# Pytest使用

通过命令行，执行pytest命令

```python
# 打开terminal
pytest # 执行所有test方法
pytest tests/test_utils.py #运行单个文件
pytest tests/test_utils.py tests/test_api.py #运行多个文件
pytest tests/test_utils.py::test_addition # 运行文件中的特定测试函数
pytest tests/test_api.py::TestUserAPI #运行文件中的特定测试类
pytest tests/test_api.py::TestUserAPI::test_get_user_profile #运行类中的特定测试方法
```



# 其他

参考学习：https://github.com/lesliechueng1996/llm-ops-api

# FAQ

### db upgrade 报错

```python
报错信息：
psycopg2.errors.UndefinedFunction: 错误:  函数 uuid_generate_v4() 不存在
LINE 3:  id UUID DEFAULT uuid_generate_v4() NOT NULL,
                         ^
HINT:  没有匹配指定名称和参数类型的函数. 您也许需要增加明确的类型转换.

解决方案：
-- 连接到你的 PostgreSQL 数据库，执行：
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```
