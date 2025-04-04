import os
# 执行数据库降级命令
os.system("flask --app app.http.app db downgrade")
# 回退到最初版本
os.system("flask --app app.http.app db downgrade base")
