# coding=utf-8

from application import app
from common.libs.Helper import ops_render
from common.libs.LogSerrvice import LogService


@app.errorhandler(404)
def error_404(e):
    LogService.addErrorLog(str(e))
    err = {'status': 404, 'msg': '很抱歉,你访问的页面不存在'}
    return ops_render('error/error.html', err)
