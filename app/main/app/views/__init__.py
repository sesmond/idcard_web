#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Title   : 模块
@File    :   __init__.py    
@Author  : vincent
@Time    : 2020/8/28 4:53 下午
@Version : 1.0 
'''
import json
import logging
import os

from flask import Blueprint, render_template, request, make_response, redirect

base_path = os.getcwd()
template_path = os.path.join(base_path, "app/main/web/templates")
static_path = os.path.join(base_path, "app/main/web/static")

# 在这里注册不同模块
idcard_app = Blueprint('idcard', __name__, url_prefix="/idcard")
case_app = Blueprint('case', __name__, url_prefix="/case")
# 通用的也做成蓝图
app = Blueprint('app', __name__,
                url_prefix="",
                template_folder=template_path,
                static_folder=static_path,
                static_url_path="/main/static")

logger = logging.getLogger(__name__)
userdata = None


@app.route("/sandbox")
def index():
    """
    首页
    @return:
    """
    version = "1.0"
    return render_template('index.html', version=version)


@app.route('/', methods=["GET"])
@app.route('/demo', methods=["GET"])
def demo_index():
    """
    demo展示页面
    @return:
    """
    return render_template("index_demo.html")


@app.route('/<regex(".*.html"):url>')
def html_request(url):
    """
    url: html url
    """
    print("请求页面：", url)
    logger.info("请求页面：%r", url)
    return render_template(url)
    # return user_auth(url)


@app.route('/login', methods=['POST'])
def login():
    print(request.form.get('username', None, str))
    logger.info("keys:>%r", request.form.fromkeys('password', str))
    username = request.form.get('username', None, str)
    password = request.form.get('password', None, str)
    language = request.form.get('language', None, str)
    if isAuthenticated(username, password):
        responseJson = {
            "ok": './',
        }
        response = make_response(json.dumps(responseJson))
        response.set_cookie('username', username, 7200)  # 超时时间1小时？
        response.set_cookie('password', password, 7200)
        response.set_cookie('language', language, 7200)
        return response
    else:
        responseJson = {
            "ok": '/browser/error',
        }
        return make_response(json.dumps(responseJson))


def user_auth(url):
    """
    用户登录验证
    """

    cookie = request.cookies
    if isAuthenticated(cookie.get('username'), cookie.get('password')):
        return render_template(url)
    else:
        return redirect("login")


def isAuthenticated(username, password):
    # TODO 应该写session 不是cookie
    global userdata
    if userdata == None:
        with open("app/browser/cfg/userdata.conf") as config:
            userdata = eval(config.read())
    try:
        if userdata[username] == password:
            return True
    except Exception:
        return False


def get_ip_address():
    if request.headers.get("X-Real-Ip"):
        return request.headers.get("X-Real-Ip")
    else:
        return request.remote_addr


# TODO 必须在启动程序中引用到才会注册，不然不会。 不会全部扫描，只扫描用到的程序。import * 不太行
from app.main.app.views import idcard_controller
