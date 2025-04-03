import os
# 执行数据库降级命令
os.system("flask --app app.http.app db downgrade")
