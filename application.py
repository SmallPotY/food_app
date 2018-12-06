# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import logging
from logging.handlers import RotatingFileHandler
import os


def create_log(app):
    fileHandler = RotatingFileHandler(app.config['LOG_FILE_FILENAME'], maxBytes=app.config['LOG_MAX_BYTES'],
                                      backupCount=app.config['LOG_BACKUP_COUNT'],
                                      encoding="UTF-8")
    streamHandler = logging.StreamHandler()
    logFormatter = logging.Formatter(app.config["LOG_FORMAT"])
    fileHandler.setLevel(eval(app.config['LOG_FILE_HANDLER']))
    fileHandler.setFormatter(logFormatter)
    streamHandler.setFormatter(logFormatter)
    streamHandler.setLevel(eval(app.config['LOG_STREAM_HANDLER']))
    app.logger.addHandler(streamHandler)
    app.logger.addHandler(fileHandler)
    app.logger.setLevel(logging.DEBUG)


class Application(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=None)
        self.config.from_pyfile('config/local_setting.py')

        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__, template_folder=os.getcwd() + '/web/templates/', root_path=os.getcwd())
manager = Manager(app)
create_log(app)

"""
模板函数
"""
from common.libs.UrlManager import UrlManager

app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
app.add_template_global(UrlManager.build_image_url, 'buildImageUrl')
