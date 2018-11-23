# coding=utf-8
from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import requests
import json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrenDate
from common.libs.member.MemberService import MemberService


@route_api.route("/member/login", methods=['GET', 'POST'])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    code = req['code'] if 'code' in req else ''

    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)

    # 获取用户微信号的openid
    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "getWeChatOpenId err"
        return jsonify(resp)

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''

    # 判断是否已经注册过，注册了返回一些信息
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = model_member.created_time = getCurrenDate()
        db.session.add(model_member)
        db.session.commit()

        # 关系绑定
        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = 'NA'
        model_bind.updated_time = model_member.created_time = getCurrenDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = "{}#{}".format(MemberService.geneAuthCode(member_info),member_info.id)
    resp['data'] = {'token':token}
    return jsonify(resp)


@route_api.route("/member/check-reg", methods=['GET', 'POST'])
def checkReg():
    resp = {'code': 200, 'msg': 'ok', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''

    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    # 获取用户微信号的openid
    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "getWeChatOpenId err"
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未绑定"
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查询导绑定信息"
        return jsonify(resp)

    token = "{}#{}".format(MemberService.geneAuthCode(member_info),member_info.id)
    resp['data'] = {'token':token}
    return jsonify(resp)
