# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, make_response, redirect, g
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.Helper import ops_render
from common.libs.UrlManager import UrlManager
from application import app, db
import json



route_user = Blueprint('user_page', __name__)


@route_user.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return ops_render("user/login.html")

    resp = {'code': 200, 'msg': "验证成功", 'data': {}}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if not login_name:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名'
        return jsonify(resp)
    if not login_pwd:
        resp['code'] = -1
        resp['msg'] = '请输入正确的密码'
        return jsonify(resp)

    user_info = User.query.filter_by(login_name=login_name).first()

    if not user_info:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名和密码 -1'
        return jsonify(resp)

    if user_info.login_pwd != UserService.genePwd(str(login_pwd), str(user_info.login_salt)):
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名和密码 -2'
        return jsonify(resp)

    response = make_response(json.dumps(resp))

    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))

    return response


@route_user.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        return ops_render("user/edit.html")

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~"
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱~"
        return jsonify(resp)

    user_info = g.current_user
    print(user_info)
    user_info.nickname = nickname
    user_info.email = email
    db.session.add(user_info)
    db.session.commit()

    return jsonify(resp)


@route_user.route("/reset-pwd")
def resetPwd():
    return ops_render("user/reset_pwd.html")


@route_user.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/user/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response
