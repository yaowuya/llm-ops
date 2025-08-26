import os

# 作用: 在项目中首次创建数据库迁移环境
# 创建 migrations/ 目录结构
# 生成 Alembic 配置文件（alembic.ini）
# 建立迁移版本追踪表
# 使用时机: 项目开始时执行一次即可
os.system("flask --app app.http.app db init")
