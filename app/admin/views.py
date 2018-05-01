# coding:utf8
from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm
from app.models import Admin, Tag, Movie, Preview
from functools import wraps
from app import db, app
from werkzeug.utils import secure_filename
import os
import uuid
import datetime


# 登录装饰器
def admin_login_require(f):
    """
    确保所有页面都在登录后才有访问权限。
    :param f: 对应页面的函数。
    :return: 返回一个检查是否登录的函数。登录时直接转到目标页面；
             未登录时跳转到登录页。
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "current_client" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    file_info = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(uuid.uuid4().hex) + file_info[-1]
    return filename


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
@admin.route("/tag/list/<int:current_page>/", methods=["GET"])
@admin_login_require
def tag_list(current_page=None):
    if current_page is None:
        current_page = 1
    page_data = Tag.query.order_by(
        Tag.add_time.desc()
    ).paginate(page=current_page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 标签删除
@admin.route("/tag/delete/<int:tag_id>/", methods=["GET"])
@admin_login_require
def tag_delete(tag_id=None):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签“%s”成功！" % (tag.name), "OK")
    return redirect(url_for('admin.tag_list', current_page=1))


# 标签编辑
@admin.route("/tag/update/<int:tag_id>/", methods=["GET", "POST"])
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
        old_tag_name = tag_old.name
        tag_old.name = data["name"]
        db.session.commit()
        flash("修改标签“%s”为“%s”成功！" % (old_tag_name, data["name"]), "OK")
        redirect(url_for('admin.tag_update', tag_id=tag_id))
    return render_template("admin/tag_update.html", form=form, tag_old=tag_old)


# 电影添加
@admin.route("/movie/add/", methods=["GET", "POST"])
@admin_login_require
def movie_add():
    form = MovieForm()
    form.movie_tag.choices = [(v.id, v.name) for v in Tag.query.all()]
    if form.validate_on_submit():
        data = form.data
        movie_file_url = secure_filename(form.movie_url.data.filename)
        cover_file_url = secure_filename(form.cover_url.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], 0o776)  # 776前面需加“0o”以十进制表示，否则默认以八进制表示
        movie_file_url = change_filename(movie_file_url)
        cover_file_url = change_filename(cover_file_url)
        form.movie_url.data.save(app.config["UP_DIR"] + movie_file_url)
        form.cover_url.data.save(app.config["UP_DIR"] + cover_file_url)
        movie = Movie(
            title=data["movie_title"],
            url=movie_file_url,
            info=data["movie_info"],
            cover=cover_file_url,
            rating=int(data["movie_rating"]),
            views=0,
            review_num=0,
            tag_id=int(data["movie_tag"]),
            area=data["movie_area"],
            release_time=data["movie_release_time"],
            length=data["movie_length"]
        )
        db.session.add(movie)
        db.session.commit()
        flash("电影“%s”添加成功！" % data["movie_title"], "OK")
        return redirect(url_for('admin.movie_add'))
    return render_template("admin/movie_add.html", form=form)


# 电影列表
@admin.route("/movie/list/<int:current_page>/", methods=["GET"])
@admin_login_require
def movie_list(current_page=None):
    if current_page is None:
        current_page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.add_time.desc()
    ).paginate(page=current_page, per_page=10)
    return render_template("admin/movie_list.html", page_data=page_data)


# 电影删除
@admin.route("/movie/delete/<int:movie_id>/", methods=["GET"])
@admin_login_require
def movie_delete(movie_id=None):
    movie = Movie.query.get_or_404(int(movie_id))
    db.session.delete(movie)
    db.session.commit()
    # 删除电影文件和封面文件
    flash("电影“%s”删除成功！" % movie.title, "OK")
    return redirect(url_for('admin.movie_list', current_page=1))


# 电影修改
@admin.route("/movie/update/<int:movie_id>/", methods=["GET", "POST"])
@admin_login_require
def movie_update(movie_id=None):
    form = MovieForm()
    movie = Movie.query.get_or_404(int(movie_id))
    if request.method == "GET":
        form.movie_info.data = movie.info
        form.movie_tag.data = movie.tag_id
        form.movie_rating.data = movie.rating
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data["movie_title"]).count()
        if movie_count == 1 and movie.title != data["movie_title"]:
            flash("电影“%s”已经存在，修改失败！" % data["movie_title"], "errors")
            return redirect(url_for('admin.movie_update', movie_id=movie_id))
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], 0o776)  # 776前面需加“0o”以十进制表示，否则默认以八进制表示
        if form.movie_url.data.filename != "":
            """更改电影视频文件名"""
            movie_file_url = secure_filename(form.movie_url.data.filename)
            movie.url = change_filename(movie_file_url)
            form.movie_url.data.save(app.config["UP_DIR"] + movie.url)
        if form.cover_url.data.filename != "":
            """更改电影封面文件名"""
            cover_file_url = secure_filename(form.cover_url.data.filename)
            movie.cover = change_filename(cover_file_url)
            form.cover_url.data.save(app.config["UP_DIR"] + movie.cover)
        movie.rating = data["movie_rating"]
        movie.tag_id = data["movie_tag"]
        movie.info = data["movie_info"]
        movie.title = data["movie_title"]
        movie.area = data["movie_area"]
        movie.length = data["movie_length"]
        movie.release_time = data["movie_release_time"]
        db.session.commit()
        flash("电影“%s”修改成功！" % data["movie_title"], "OK")
        return redirect(url_for('admin.movie_update', movie_id=movie_id))
    return render_template("admin/movie_update.html", form=form, movie=movie)


@admin.route("/preview/add/", methods=["GET", "POST"])
@admin_login_require
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data

    return render_template("admin/preview_add.html", form=form)


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
