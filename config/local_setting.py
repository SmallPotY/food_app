# coding=utf-8



SERVER_PORT = 8888
SERVER_HOST = '127.0.0.1'
DEBUG = True


# 页数显示
PAGE_SIZE = 50
PAGE_DISPLAY = 10

AUTH_COOKIE_NAME = "MY_COOKIE"


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
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True


## 过滤url
IGNORE_URLS = [
    "^/user/login"
]

IGNORE_CHECK_LOGIN_URLS=[
    "^/static",
    "^/favicon.ico"
]