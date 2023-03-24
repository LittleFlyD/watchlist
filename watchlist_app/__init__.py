# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# APP
app = Flask(__name__)

# LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from .models import User

    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


@app.context_processor
def inject_user():
    from .models import User

    user = User.query.first()
    return dict(user=user)


# Flask-WTF 默认支持CSRF（跨站请求伪造）保护，
# 只需要在程序中设置一个密钥。
# Flask-WTF使用这个密钥生成加密令牌，再用令牌验证表单中数据的真伪
app.config["SECRET_KEY"] = "dev"  # 等同于 app.secret_key = 'dev'

# DB
if "unittest" in sys.modules.keys():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(os.path.dirname(app.root_path), "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app


# 在构造文件中，为了让视图函数、错误处理函数和命令函数注册到程序实例上，我们需要在这里导入这几个模块。
# 但是因为这几个模块同时也要导入构造文件中的程序实例，为了避免循环依赖（A 导入 B，B 导入 A），
# 我们把这一行导入语句放到构造文件的结尾。
# 同样的，load_user() 函数和 inject_user() 函数中使用的模型类也在函数内进行导入。
from . import views, errors, commands
