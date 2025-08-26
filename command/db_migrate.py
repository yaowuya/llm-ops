import os

# 作用: 自动检测模型变化并生成迁移脚本
# 比较当前模型与数据库结构的差异
# 在 migrations/versions/ 下生成新的迁移文件
# 注意: 这里有个路径不一致问题（app.server.app vs app.http.app）
os.system("flask --app app.server.app db migrate")
