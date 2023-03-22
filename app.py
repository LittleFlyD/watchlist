from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

name = 'Hiroo Chen'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name=name, movies=movies)


@app.route('/user/<user_name>')
def user_page(user_name):
    # 注意 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，
    # 需要使用 MarkupSafe（Flask 的依赖之一）提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;。
    # 这样在返回响应时浏览器就不会把它们当做代码执行。
    return f'<h1>Hello {escape(user_name)}! Welcome to my Film-Watchlist</h1><img ' \
           f'src="http://helloflask.com/totoro.gif">'

