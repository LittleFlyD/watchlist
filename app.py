from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def hello():
    return '<h1>Hello! Welcome to my Film-Watchlist</h1><img src="http://helloflask.com/totoro.gif">'


@app.route('/user/<name>')
def user_page(name):
    # 注意 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，
    # 需要使用 MarkupSafe（Flask 的依赖之一）提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;。
    # 这样在返回响应时浏览器就不会把它们当做代码执行。
    return f'<h1>Hello {escape(name)}! Welcome to my Film-Watchlist</h1><img src="http://helloflask.com/totoro.gif">'

