# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError
from app.models import Admin


class LoginForm(FlaskForm):
    """管理员登录表单。"""
    account = StringField(
        "username",  # 此处不能写成：label = "username"，否则会报错。
        validators=[
            DataRequired("请输入帐号！")
        ],
        description="管理员帐号",
        render_kw={
            "class": "form-control",
            "placeholder": "您的账号",
            # "required": "required"  # H5 效果，若不加则显示 validators 中的内容。
        }
    )
    password = PasswordField(
        "password",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "您的密码",
            # "required": "required"  # H5 效果，若不加则显示 validators 中的内容。
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self, field):
        account = field.data
        _counter = Admin.query.filter_by(name=account).count()
        if _counter == 0:
            raise ValidationError("账号不存在，请输入正确的账号。")
