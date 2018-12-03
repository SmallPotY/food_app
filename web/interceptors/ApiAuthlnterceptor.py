# coding=utf-8
from application import app
from flask import request, g, jsonify
from common.models.member.Member import Member
from common.libs.member.MemberService import MemberService

import re

"""
api 认证
"""


@app.before_request
def before_request():
    api_ignore_urls = app.config['API_IGNORE_URLS']
    path = request.path

    if '/api' not in path:
        return

    member_info = check_member_login()

    g.member_info = None
    if member_info:
        g.member_info = member_info

    pattern = re.compile('%s' % "|".join(api_ignore_urls))
    if pattern.match(path):
        return

    if not member_info:
        resp = {'code': -1, 'msg': '未登陆~', 'data': {}}
        return jsonify(resp)

    return


def check_member_login():
    """登陆验证"""
    auth_cookie = request.headers.get('Authorization')
    print('auth_cookie',auth_cookie)
    if auth_cookie is None:
        return False  # 没有cookie

    auth_info = auth_cookie.split('#')
    if len(auth_info) != 2:
        return False  # cookie不符


    try:
        member_info = Member.query.filter_by(id=auth_info[1]).first()
    except Exception:
        return False  # 数据库异常

    if auth_info is None:
        return False  # 查无此人

    if auth_info[0] != MemberService.geneAuthCode(member_info):
        return False

    if member_info.status != 1:
        return False  # 账号无效

    return member_info
