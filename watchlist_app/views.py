from flask import request, redirect, url_for, flash, render_template
from flask_login import login_user, login_required, logout_user, current_user
from markupsafe import escape

from watchlist_app import db, app
from watchlist_app.forms import AddItemForm
from watchlist_app.models import Movie, User


# Routes
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    form = AddItemForm()
    if request.method == "POST":
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for("index"))  # 重定向到主页
    if form.validate_on_submit():
        title = form.title.data
        year = form.year.data
        # 验证数据
        if not title or not year or len(title) > 60 or len(year) > 4:
            flash("Invalid input.")  # 显示错误提示
            return redirect(url_for("index"))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash("Item created.")  # 显示成功创建的提示
        return redirect(url_for("index"))  # 重定向回主页

    movies = Movie.query.all()
    return render_template("index.html", movies=movies, form=form)


@app.route("/movie/edit/<int:movie_id>", methods=["GET", "POST"])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":  # 处理编辑表单的提交请求
        title = request.form["title"]
        year = request.form["year"]

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash("Invalid input.")
            return redirect(url_for("edit", movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash("Item updated.")
        return redirect(url_for("index"))  # 重定向回主页

    return render_template("edit.html", movie=movie)  # 传入被编辑的电影记录


# -*- coding: utf-8 -*-


@app.route("/movie/delete/<int:movie_id>", methods=["POST"])  # 限定只接受 POST 请求
@login_required  # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash("Item deleted.")
    return redirect(url_for("index"))  # 重定向回主页


@app.route("/user/<user_name>")
def user_page(user_name):
    # 注意 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，
    # 需要使用 MarkupSafe（Flask 的依赖之一）提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;。
    # 这样在返回响应时浏览器就不会把它们当做代码执行。
    return (
        f"<h1>Hello {escape(user_name)}! Welcome to my Film-Watchlist</h1><img "
        f'src="http://helloflask.com/totoro.gif">'
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Invalid input.")
            return redirect(url_for("login"))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash("Login success.")
            return redirect(url_for("index"))  # 重定向到主页

        flash("Invalid username or password.")  # 如果验证失败，显示错误消息
        return redirect(url_for("login"))  # 重定向回登录页面

    return render_template("login.html")


@app.route("/logout")
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash("Goodbye.")
    return redirect(url_for("index"))  # 重定向回首页


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        name = request.form["name"]

        if not name or len(name) > 20:
            flash("Invalid input.")
            return redirect(url_for("settings"))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash("Settings updated.")
        return redirect(url_for("index"))

    return render_template("settings.html")
