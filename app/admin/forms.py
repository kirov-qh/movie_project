# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
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


class TagForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired("标签名称不能为空，请重新输入！")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称:"
        }
    )
    submit = SubmitField(
        '添加标签',
        render_kw={
            "class": "btn btn-primary"
        }
    )
