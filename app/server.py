import os, logging, traceback
from flask import Flask, request
from werkzeug.routing import BaseConverter
from threading import current_thread

from app.main.app.utils import logger as log
# from app.main import conf


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


# 参考：https://www.cnblogs.com/haolujun/p/9778939.html
# app = Flask(__name__,static_folder="./web/static",template_folder="./web/templates")
app = Flask(__name__)
# app = Flask(__name__, root_path=os.path.join(os.getcwd(), "app/browser/web"))
# TODO 可能不同模块用不同的
app.jinja_env.globals.update(zip=zip)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.url_map.converters['regex'] = RegexConverter


def _logger():
    return logging.getLogger(__name__)


@app.errorhandler(500)
def internal_server_error_500(e):
    print("异常发生：")
    traceback.print_exc()
    _logger().error("====================================异常堆栈为====================================", exc_info=True)
    _logger().info("==================================================================================")


# 每个URL请求之前，打印请求日志
@app.before_request
def before_request():
    if request.headers.get("X-Real-Ip"):
        _logger().info("ip:%r,access:%r", request.headers.get("X-Real-Ip"), request.path)
    else:
        _logger().info("local ip:%r,access:%r,%r", request.remote_addr, request.path, request.method)


# @app.after_request
# def process_response(response):
#     _logger().info("local ip:%r,access:%r,end", request.remote_addr, request.path)
#     return response


def startup(app):
    # log.init(conf.system_config.log_dir)
    _logger().info("初始化参数开始！")
    # conf.init_arguments()
    _logger().info("初始化参数结束！")
    # init_log()
    _logger().info('启动环境:,子进程:%s,父进程:%s,线程:%r',  os.getpid(), os.getppid(), current_thread())
    # 初始化各种变量（全局）
    # server_utils.init_single(conf.MODE)
    # 记录系统根目录
    # if conf.MODE == conf.MODE_DEBUG:
    #     root_path = app.root_path  # 指向 web 目录
    #     root_path, _ = os.path.split(root_path)  # 需要返回一级，到项目目录
    #     conf.root_path = root_path  # 记录web server的root路径
    #     _logger().info("Debug模式下，系统根路径[root_path]设置为：%s", conf.root_path)
    # else:
    # _logger().info("系统根路径[root_path]设置为：%s", conf.root_path)

    # 注册所有蓝图
    regist_blueprint(app)

    _logger().info("注册完所有路由：\n %r", app.url_map)
    _logger().info("系统启动完成")


def regist_blueprint(app):
    """
     注册所有蓝图 TODO  想办法如何一键式解决,保证开闭
    :param app:
    :return:
    """
    from app.main.app.views import idcard_app
    from app.main.app.views import app as main_app
    app.register_blueprint(main_app)
    app.register_blueprint(idcard_app)

print("启动服务器...")
startup(app)
