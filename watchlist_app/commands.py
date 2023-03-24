# -*- coding: utf-8 -*-
import click

from watchlist_app import app, db
from .models import Movie, User


@app.cli.command()  # 注册为命令，可以传入name参数来自定义命令
@click.option("--drop", is_flag=True, help="Create after drop.")  # 设置选项
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")


@app.cli.command()
def forge():
    db.create_all()

    movies = [
        {"title": "My Neighbor Totoro", "year": "1988"},
        {"title": "Dead Poets Society", "year": "1989"},
        {"title": "A Perfect World", "year": "1993"},
        {"title": "Leon", "year": "1994"},
        {"title": "Mahjong", "year": "1996"},
        {"title": "Swallowtail Butterfly", "year": "1996"},
        {"title": "King of Comedy", "year": "1999"},
        {"title": "Devils on the Doorstep", "year": "1999"},
        {"title": "WALL-E", "year": "2008"},
        {"title": "The Pork of Music", "year": "2012"},
    ]
    for movie in movies:
        m = Movie(title=movie["title"], year=movie["year"])
        db.session.add(m)
    db.session.commit()

    click.echo("Done.")


@app.cli.command()
@click.option("--username", prompt=True, help="The username used to login.")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="The password used to login.")
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo("Updating user...")
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo("Creating user...")
        user = User(username=username, name="Admin")
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo("Done.")
