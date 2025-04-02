from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    query = StringField("query", validators=[
        DataRequired(message="请输入用户问题"),
        Length(max=2000, message="用户问题不能超过2000字符")
    ])
