import os

# 作用: 将数据库结构升级到最新版本
#
# 按顺序执行所有未应用的迁移脚本
# 更新数据库结构（表、字段、索引等）
os.system("flask --app app.http.app db upgrade")
