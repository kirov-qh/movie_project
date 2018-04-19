# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin, Tag

movie_tag_list = Tag.query.all()


class LoginForm(FlaskForm):
    """管理员登录表单。"""
    account = StringField(
        label="username",  # 此处不能写成：label="username"，否则会报错。
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
        label="password",
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
        description="标签名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称:"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )
    update_submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary"
        }
    )


class MovieForm(FlaskForm):
    movie_title = StringField(
        label="片名",
        validators=[
            DataRequired("影片名称不能为空，请重新输入！")
        ],
        description="电影名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入影片名称:"
        }
    )
    movie_url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件！")
        ],
        description="电影媒体文件"
    )
    movie_info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("影片简介不能为空，请重新输入！")
        ],
        description="电影简介",
        render_kw={
            "class": "form-control",
            "rows": "10"
        }
    )
    cover_url = FileField(
        label="封面",
        validators=[
            DataRequired("请上传电影封面！")
        ],
        description="电影封面"
    )
    movie_rating = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择电影星级！")
        ],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="电影星级",
        render_kw={
            "class": "form-control"
        }
    )
    movie_tag = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择电影对应的标签！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in movie_tag_list],
        description="电影标签",
        render_kw={
            "class": "form-control"
        }
    )
    movie_area = StringField(
        label="地区",
        validators=[
            DataRequired("影片上映地区不能为空，请重新输入！")
        ],
        description="电影上映地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入电影上映地区:"
        }
    )
    movie_length = StringField(
        label="片长",
        validators=[
            DataRequired("影片长度不能为空，请重新输入！")
        ],
        description="电影片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入电影片长:"
        }
    )
    movie_release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("上映时间错误，请重新输入！")
        ],
        description="电影上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入电影上映时间:",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )
    update_submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary"
        }
    )
