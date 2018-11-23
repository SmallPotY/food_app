# coding=utf-8
from common.models.log.AppAccessLog import AppAccessLog
from common.models.log.AppErrLog import AppErrorLog
from common.libs.Helper import getCurrenDate
from application import app, db
from flask import request, g
import json


class LogService():
    """日志系统"""

    @staticmethod
    def addAccessLog():

        target = AppAccessLog()
        target.target_url = request.url         # 转入url
        target.referer_url = request.referrer   # 原url
        target.ip = request.remote_addr         # ip地址
        target.query_params = json.dumps(request.values.to_dict())      # 访问参数
        if 'current_user' in g and g.current_user is not None:
            target.uid = g.current_user.uid                         # 用户
        target.ua = request.headers.get("User-Agent")               # 请求头
        target.created_time = getCurrenDate()                       # 访问时间
        db.session.add(target)
        db.session.commit()
        return True


    @staticmethod
    def addErrorLog(e):
        target = AppErrorLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.query_params = json.dumps(request.values.to_dict())
        target.content = e
        target.created_time = getCurrenDate()
        db.session.add(target)
        db.session.commit()
        return True
