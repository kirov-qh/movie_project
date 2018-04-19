# coding:utf8
from datetime import datetime
from app import db

class User(db.Model):
    """
    Informations of users.
    """
    __tablename__ = "user"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # user number
    name = db.Column(db.String(100), unique=True)  # username
    password = db.Column(db.String(100))  # user's password
    email = db.Column(db.String(100), unique=True)  # user's email address
    phone = db.Column(db.String(11), unique=True)  # user's mobile phone number
    info = db.Column(db.Text)  # user's signature
    avatar = db.Column(db.String(255), unique=True)  # user's profile picture
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # registration time
    uuid = db.Column(db.String(255), unique=True)  # user's unique identifier
    user_logs = db.relationship('Userlog', backref='user')  # key used to associate with user log table
    comments = db.relationship('Comment', backref='user')  # key used to associate with comment table
    collections = db.relationship('Collection', backref='user')  # key used to associate with collection table

    def __repr__(self):
        return "<User %r>" % self.name


class Userlog(db.Model):
    """
    Log when users sign in.
    """
    __tablename__ = "userlog"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # log number
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # corresponding user connected with the user table
    ip = db.Column(db.String(100))  # the corresponding users' IP address
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # log generation time

    def __repr__(self):
        return "<Userlog %r>" % self.id


class Tag(db.Model):
    """
    Tag of the movies.
    """
    __tablename__ = "tag"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # tag number
    name = db.Column(db.String(100), unique=True)  # name of tag
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # tag generation time
    movies = db.relationship("Movie", backref='tag')  # key used to associate with tag table

    def __repr__(self):
        return "<Tag %r>" % self.name


class Movie(db.Model):
    """
    Definition of movie information.
    """
    __tablename__ = "movie"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # movie number
    title = db.Column(db.String(255), unique=True)  # title of the movie
    url = db.Column(db.String(255), unique=True)  # movie playback link
    info = db.Column(db.Text)  # introduction of the movie
    cover = db.Column(db.String(255), unique=True)  # cover of the movie
    rating = db.Column(db.SmallInteger)  # rating of the movie
    views = db.Column(db.BigInteger)  # number of times played
    review_num = db.Column(db.BigInteger)  # number of reviews
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # corresponding tag connected with the tag table
    area = db.Column(db.String(255))  # movie release area
    release_time = db.Column(db.Date)  # movie release time
    length = db.Column(db.String(100))  # the length of the movie
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # time when the movie added to the website
    comments = db.relationship('Comment', backref='movie')  # key used to associate with comment table
    collections = db.relationship('Collection', backref='movie')  # key used to associate with collection table

    def __repr__(self):
        return "<Movie %r>" % self.title


class Preview(db.Model):
    """
    Movie preview.
    """
    __tablename__ = "preview"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # preview number
    title = db.Column(db.String(255), unique=True)  # title of the movie preview
    cover = db.Column(db.String(255), unique=True)  # cover of the movie preview
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # time when the preview added to the website

    def __repr__(self):
        return "<Preview %r>" % self.title


class Comment(db.Model):
    """
    Movie comment.
    """
    __tablename__ = "comment"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # comment number
    content = db.Column(db.Text)  # content of the comment
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # commented movie
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # user who submitted the comment
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # time when the comment submitted

    def __repr__(self):
        return "<Comment %r>" % self.id


class Collection(db.Model):
    """
    Movie collection.
    """
    __tablename__ = "collection"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # collection number
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # movie which is collected
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # user who collect this movie
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # time when the movie is bookmarked

    def __repr__(self):
        return "<Collection %r>" % self.id


class Authority(db.Model):
    """
    The definition of authorities.
    """
    __tablename__ = "authority"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # authority number
    name = db.Column(db.String(100), unique=True)  # authority name
    url = db.Column(db.String(255), unique=True)  # the routing address corresponded to the authority
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # time when the authority is added

    def __repr__(self):
        return "<Authority %r>" % self.name


class Role(db.Model):
    """
    The definition of roles.
    """
    __tablename__ = "role"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # role number
    name = db.Column(db.String(100), unique=True)  # role name
    authorities = db.Column(db.String(600))  # The authorities granted to the role
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # time when the role is added

    def __repr__(self):
        return "<Role %r>" % self.name


class Admin(db.Model):
    """
    The definition of admins.
    """
    __tablename__ = "admin"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # admin number
    name = db.Column(db.String(100), unique=True)  # admin name
    password = db.Column(db.String(100))  # admin password
    is_super = db.Column(db.SmallInteger)  # whether it is a super administrator, 0 is super administrator
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # the role to which the administrator belongs
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # time when the admin is added
    adminlogs = db.relationship('Adminlog', backref='admin')  # key used to associate with administrator log table
    operationlogs = db.relationship('Operationlog',
                                    backref='admin')  # key used to associate with administrator operations log table

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)


class Adminlog(db.Model):
    """
    Log when administrators sign in.
    """
    __tablename__ = "adminlog"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # log number
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # corresponding user connected with the admin table
    ip = db.Column(db.String(100))  # the corresponding administrators' IP address
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # log generation time

    def __repr__(self):
        return "<Adminlog %r>" % self.id


class Operationlog(db.Model):
    """
    Log when administrators sign in.
    """
    __tablename__ = "operationlog"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # log number
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # corresponding user connected with the admin table
    ip = db.Column(db.String(100))  # the corresponding administrators' IP address
    reason = db.Column(db.String(100))  # the reason why administrator do this operation
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # log generation time

    def __repr__(self):
        return "<Operationlog %r>" % self.id


# if __name__ == "__main__":
#     # 创建全部表，在创建数据库后仅能运行一次
#     db.create_all()
#     # 创建超级管理员角色，亦只能运行一次
#     role = Role(
#         name="超级管理员",
#         authorities=""
#     )
#     db.session.add(role)
#     db.session.commit()
#     # 创建管理员账号，亦只能运行一次
#     from werkzeug.security import generate_password_hash
#
#     admin = Admin(
#         name="Peter",
#         password=generate_password_hash("131072"),
#         is_super=0,
#         role_id=1
#     )
#     db.session.add(admin)
#     db.session.commit()
