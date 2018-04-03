# -*- coding: utf-8 -*-

# 导入一些基础库。有些之后并没有用到，但还是懒得删了，
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import json
import gevent

# 定义好app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['JSON_AS_ASCII'] = False

# 能不能实现WebSocket的关键了，不定义socket后面没法玩
sockietio = SocketIO(app)

# 因为项目很小所以就不用数据库了，直接用列表吧
adult_list = []
pass_list = []
del_list = []


# 由于水平有限，需求也不多，所以只有一个html
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/show')
def show():
    return render_template("show.html")

@app.route('/adult')
def adult():
    return render_template("adult.html")


# 这个就是关键了，用来接受客户端emit来的内容，因为只是一个用一次的应用，加入列表留底审核
@sockietio.on('send_message')
def send_message(adult_data):
    adult_list.append(adult_data)
    print(adult_data + "\n这是第：" + str(len(pass_list) + len(del_list) + len(adult_list)) + "条发送的内容")


# 将之前客户端的传来的所有数据，广播给后台
@sockietio.on('request_list')
def get_list():
    emit('get_list',adult_list)

# 将后台审核过的数据广播给所有在线的客户端
@sockietio.on('pass_message')
def pass_message(pass_data):
    print(pass_data)
    if (pass_data in adult_list):
        adult_list.remove(pass_data)
        pass_list.append(pass_data)
        print(pass_data + "\n这是第：" + str(len(pass_list)) + "条通过的内容")
        emit('get_message', pass_data, broadcast=True)
    else:
        print("出现异常")

# 将未审核通过的移除
@sockietio.on('del_message')
def del_message(del_data):
    if(del_data in adult_list):
        adult_list.remove(del_data)
        del_list.append(del_data)
        print(del_data + "\n这是第：" + str(len(del_list)) + "条删除的内容")
    else:
        print("出现异常")

# 和以前flask不一样的是启动方式不能写成app.run()了，要写成SocketIO的启动方式，因为服务器直接用的flask的,没有什么wsgi，所以host改成0.0.0.0，端口还是50000
if __name__ == '__main__':
    sockietio.run(app, host='0.0.0.0')
