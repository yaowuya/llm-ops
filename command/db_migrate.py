import os

# 生成迁移脚本
os.system("flask --app app.server.app db migrate")
