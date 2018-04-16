# coding:utf8
from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm
from app.models import Admin, Tag
from functools import wraps
from app import db


def admin_login_require(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "current_client" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@admin.route("/")
@admin_login_require
def index():
    return render_template("admin/index.html")


# 登录
@admin.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        current_client = Admin.query.filter_by(name=data["account"]).first()
        if not current_client.check_password(data["password"]):
            flash("密码错误，请重新输入！")
            return redirect(url_for("admin.login"))
        session["current_client"] = data["account"]
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout/")
@admin_login_require
def logout():
    session.pop("current_client", None)
    return redirect(url_for("admin.login"))


@admin.route("/password/")
@admin_login_require
def password():
    return render_template("admin/password.html")


# 标签添加
@admin.route("/tag/add/", methods=["GET", "POST"])
@admin_login_require
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag_counter = Tag.query.filter_by(name=data["name"]).count()
        if tag_counter == 1:
            flash("标签“%s”已经存在！" % (data["name"]), "errors")
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        flash("添加标签“%s”成功！" % (data["name"]), "OK")
        redirect(url_for('admin.tag_add'))
    return render_template("admin/tag_add.html", form=form)


# 标签列表
@admin.route("/tag/list/<int:current_page>", methods=["GET"])
@admin_login_require
def tag_list(current_page=None):
    if current_page is None:
        current_page = 1
    page_data = Tag.query.order_by(
        Tag.add_time.desc()
    ).paginate(page=current_page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 标签删除
@admin.route("/tag/delete/<int:tag_id>", methods=["GET"])
@admin_login_require
def tag_delete(tag_id=None):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签“%s”成功！" % (tag.name), "OK")
    return redirect(url_for('admin.tag_list', current_page=1))


# 标签编辑
@admin.route("/tag/update/<int:tag_id>", methods=["GET", "POST"])
@admin_login_require
def tag_update(tag_id=None):
    form = TagForm()
    tag_old = Tag.query.get_or_404(tag_id)
    if form.validate_on_submit():
        data = form.data
        tag_counter = Tag.query.filter_by(name=data["name"]).count()
        if tag_old.name != data["name"] and tag_counter == 1:
            # 旧标签的名字和新标签的名字不同且新标签的名字已经存在
            flash("标签“%s”已经存在！" % (data["name"]), "errors")
            return redirect(url_for('admin.tag_update', tag_id=tag_id))
        old_tag_name =tag_old.name
        tag_old.name = data["name"]
        db.session.commit()
        flash("修改标签“%s”为“%s”成功！" % (old_tag_name, data["name"]), "OK")
        redirect(url_for('admin.tag_update', tag_id=tag_id))
    return render_template("admin/tag_update.html", form=form, tag_old=tag_old)


@admin.route("/movie/add/")
@admin_login_require
def movie_add():
    return render_template("admin/movie_add.html")


@admin.route("/movie/list/")
@admin_login_require
def movie_list():
    return render_template("admin/movie_list.html")


@admin.route("/preview/add/")
@admin_login_require
def preview_add():
    return render_template("admin/preview_add.html")


@admin.route("/preview/list/")
@admin_login_require
def preview_list():
    return render_template("admin/preview_list.html")


@admin.route("/user/list/")
@admin_login_require
def user_list():
    return render_template("admin/user_list.html")


@admin.route("/user/view/")
@admin_login_require
def user_view():
    return render_template("admin/user_view.html")


@admin.route("/comments/list/")
@admin_login_require
def comments_list():
    return render_template("admin/comments_list.html")


@admin.route("/collection/list/")
@admin_login_require
def collection_list():
    return render_template("admin/collection_list.html")


@admin.route("/operations/log/list/")
@admin_login_require
def operations_log_list():
    return render_template("admin/operations_log_list.html")


@admin.route("/admin_login/log/list/")
@admin_login_require
def admin_login_log_list():
    return render_template("admin/admin_login_log_list.html")


@admin.route("/user_login/log/list/")
@admin_login_require
def user_login_log_list():
    return render_template("admin/user_login_log_list.html")


@admin.route("/role/add/")
@admin_login_require
def role_add():
    return render_template("admin/role_add.html")


@admin.route("/role/list/")
@admin_login_require
def role_list():
    return render_template("admin/role_list.html")


@admin.route("/authority/add/")
@admin_login_require
def authority_add():
    return render_template("admin/authority_add.html")


@admin.route("/authority/list/")
@admin_login_require
def authority_list():
    return render_template("admin/authority_list.html")


@admin.route("/admin/add/")
@admin_login_require
def admin_add():
    return render_template("admin/admin_add.html")


@admin.route("/admin/list/")
@admin_login_require
def admin_list():
    return render_template("admin/admin_list.html")
