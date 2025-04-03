import os

# 执行数据库升级命令
os.system("flask --app app.http.app db upgrade")
