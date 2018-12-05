# coding=utf-8

# ----------------------------------------------------------
SERVER_PORT = 8888
SERVER_HOST = '127.0.0.1'
DEBUG = True

# ----------------------页数显示-----------------------------
PAGE_SIZE = 50
PAGE_DISPLAY = 10

# cookie 密钥
AUTH_COOKIE_NAME = "MY_COOKIE"

# JS版本号
# RELEASE_VERSION = '1.0'

# ----------------------数据库配置----------------------------

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'smallpot'
PASSWORD = 'yj'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'food'
SQLALCHEMY_ENCODING = 'utf-8'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                          PORT, DATABASE)
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

# ----------------------url过滤-----------------------------

# 过滤url
IGNORE_URLS = [
    "^/user/login",
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

API_IGNORE_URLS = [
    "^/api"
]

# ---------------------状态值-----------------------------
STATUS_MAPPING = {
    "1": "正常",
    "0": "无效"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0": "订单已关闭",
    "1": "支付成功",
    "-8": "待支付",
    "-7": "待发货",
    "-6": "待确认",
    "-5": "待评价"
}

# --------------------上传配置-----------------------------
UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

# ---------------------小程序密钥------------------------------
MINA_APP = {
    'AppID': 'wx542fcc3a513f6b75',
    'AppKey': 'd07b6e7413cbe494c422c82d74b01e96',
    'paykey': 'xxxxxxxxxxxxxx换自己的',
    'mch_id': 'xxxxxxxxxxxx换自己的',
    'callback_url': '/api/order/callback'
}

APP = {
    'domain': 'http://127.0.0.1:8888'
}
