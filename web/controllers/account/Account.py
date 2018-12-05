# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.User import User
from common.models.log.AppAccessLog import AppAccessLog
from sqlalchemy import or_
from application import app, db

route_account = Blueprint('account_page', __name__)


@route_account.route("/index")
def index():
    resp_data = {}
    req = request.values
    query = User.query

    if 'mix_kw' in req:
        rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])), User.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))

    page = int(req['p']) if ('p' in req and req['p']) else 1
    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    user_list = query.order_by(User.uid.desc()).all()[offset:limit]
    resp_data['list'] = user_list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("account/index.html", resp_data)





@route_account.route("/info")
def info():
    resp_data = {}

    req = request.args
    uid = int(req.get('id', 0))
    redirect_url = UrlManager.buildUrl("/account/index")

    if uid < 1:
        return redirect(redirect_url)

    info = User.query.filter_by(uid=uid).first()
    if not info:
        return redirect(redirect_url)

    # log = AppAccessLog.query.filter(AppAccessLog.uid==uid).order_by(AppAccessLog.created_time.desc()).all()
    log = AppAccessLog.query.filter(AppAccessLog.uid==uid)

    page = int(req['p']) if ('p' in req and req['p']) else 1
    page_params = {
        'total': log.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    log_list = log.order_by(AppAccessLog.uid.desc()).all()[offset:limit]
    print(log_list)
    resp_data['info'] = info
    resp_data['log_list'] = log_list
    resp_data['pages'] = pages

    return ops_render("account/info.html", resp_data)


@route_account.route("/set", methods=['GET', 'POST'])
def set():
    default_pdw = "******"

    if request.method == 'GET':
        resp_data = {}
        req = request.args
        uid = int(req.get("id", 0))
        user_info = None
        if uid:
            user_info = User.query.filter_by(uid=uid).first()
        resp_data['user_info'] = user_info

        return ops_render("account/set.html", resp_data)
    resp = {"code": 200, "msg": "操作成功~"}
    req = request.values

    id = req['id'] if 'id' in req else 0

    nickname = req['nickname'] if 'nickname' in req else None
    email = req['email'] if 'email' in req else None
    mobile = req['mobile'] if 'mobile' in req else None
    login_name = req['login_name'] if 'login_name' in req else None
    login_pwd = req['login_pwd'] if 'login_pwd' in req else None

    if nickname is None:
        resp['code'] = -1
        resp['msg'] = '请输入昵称'
        return jsonify(resp)
    if email is None:
        resp['code'] = -1
        resp['msg'] = '请输入邮箱'
        return jsonify(resp)
    if mobile is None:
        resp['code'] = -1
        resp['msg'] = '请输入手机号码'
        return jsonify(resp)
    if login_name is None:
        resp['code'] = -1
        resp['msg'] = '请输入登陆用户'
        return jsonify(resp)
    if login_pwd is None:
        resp['code'] = -1
        resp['msg'] = '请输入密码'
        return jsonify(resp)

    # filter需要写入对象，可接受较复杂的算式    filter_by不需要写入对象
    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = '该登陆名已存在，请换一个试试~'
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()

    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.geneSalt()

    model_user.nickname = nickname
    model_user.email = email
    model_user.mobile = mobile
    model_user.login_name = login_name
    if login_pwd != default_pdw:
        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
    model_user.updated_time = getCurrentDate()

    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)


@route_account.route("/ops", methods=['POST'])
def ops():
    resp = {'code': 200, 'msg': "操作成功", 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择所要操作的账号~"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()

    if not user_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在"
        return jsonify(resp)

    if act == 'remove':
        user_info.status = 0
    elif act == "recover":
        user_info.status = 1

    user_info.update_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)
