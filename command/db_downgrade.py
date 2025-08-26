import os

# 作用: 回滚数据库结构到之前的版本
#
# 第一个命令：回退到上一个版本
# 第二个命令：回退到初始状态（清空所有迁移）
# 执行数据库降级命令
os.system("flask --app app.http.app db downgrade")
# 回退到最初版本
os.system("flask --app app.http.app db downgrade base")
