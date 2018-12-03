# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrenDate
from common.libs.UrlManager import UrlManager
from common.models.member.Member import Member
from application import app, db

route_member = Blueprint('member_page', __name__)


@route_member.route("/index")
def index():
    resp = {}

    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    query = Member.query

    if 'mix_kw' in req:
        query = query.filter(Member.nickname.ilike("%{}%".format(req['mix_kw'])))

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Member.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    data_list = query.order_by(Member.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    resp['list'] = data_list
    resp['pages'] = pages
    resp['current'] = 'index'
    resp['status_mapping'] = app.config['STATUS_MAPPING']
    resp['search_con'] = req
    return ops_render("member/index.html", resp)


@route_member.route("/info")
def info():
    resp = {}

    req = request.args

    id = int(req.get("id", 0))
    if id < 1:
        return redirect(UrlManager.buildUrl("/member/index"))

    info = Member.query.filter_by(id=id).first()

    if not info:
        return redirect(UrlManager.buildUrl("/member/index"))

    resp['info'] = info
    resp['current'] = 'index'
    return ops_render("member/info.html", resp)


@route_member.route("/set", methods=['GET', 'POST'])
def set():
    if request.method == 'GET':
        resp = {'current': 'index'}
        req = request.args
        id = int(req.get('id', 0))
        if id < 1:
            return redirect(UrlManager.buildUrl("/member/index"))
        info = Member.query.filter_by(id=id).first()
        if not info:
            return redirect(UrlManager.buildUrl("/member/index"))

        if info.status != 1:
            return redirect(UrlManager.buildUrl("/member/index"))

        resp['info'] = info
        return ops_render("member/set.html", resp)

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的昵称"
        return jsonify(resp)

    member_info = Member.query.filter_by(id=id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "指定会员不存在"
    member_info.nickname = nickname
    member_info.updated_time = getCurrenDate()
    db.session.add(member_info)
    db.session.commit()

    return jsonify(resp)


@route_member.route("/comment")
def comment():
    return ops_render("member/comment.html")


@route_member.route("/ops", methods=['POST'])
def ops():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''

    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择操作账号~~"
        return jsonify(resp)

    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    member_info = Member.query.filter_by(id=id).first()

    if not member_info:
        resp['code'] = -1
        resp['msg'] = '指定会员不存在~~'
        return jsonify(resp)

    if act == 'remove':
        member_info.status = 0
    elif act == 'recover':
        member_info.status = 1

    member_info.updated_time = getCurrenDate()
    db.session.add(member_info)
    db.session.commit()

    return jsonify(resp)


@route_member.route('/member/share', methods=['GET', 'POST'])
def member_share():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    return jsonify(resp)
