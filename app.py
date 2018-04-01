# -*- coding: utf-8 -*-

# 导入一些基础库。有些之后并没有用到，但还是懒得删了，
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import json
import gevent
import geventwebsocket

# 定义好app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['JSON_AS_ASCII'] = False

# 能不能实现WebSocket的关键了，不定义socket后面没法玩
sockietio = SocketIO(app)


# 由于水平有限，需求也不多，所以只有一个html
@app.route('/')
def hello_world():
    return render_template("index.html")


# 这个就是关键了，用来接受客户端emit来的内容，因为只是一个用一次的应用，所以对数据传输没有做什么处理
@sockietio.on('my event')
def handle_my_custom_event(data):
    print(data)
# 将之前客户端的传来的数据，广播给所有在线的客户端
    emit('my response', data, broadcast=True)

# 和以前flask不一样的是启动方式不能写成app.run()了，要写成SocketIO的启动方式，因为服务器直接用的flask的,没有什么wsgi，所以host改成0.0.0.0，端口还是50000
if __name__ == '__main__':
    sockietio.run(app, host='0.0.0.0')
