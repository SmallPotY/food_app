# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify

from application import app, db
from common.libs.Helper import ops_render, getCurrenDate
from common.models.food.FoodCat import FoodCat

route_food = Blueprint('food_page', __name__)


@route_food.route("/index")
def index():
    return ops_render("food/index.html")


@route_food.route("/info")
def info():
    return ops_render("food/info.html")


@route_food.route("/set")
def set():
    return ops_render("food/set.html")


@route_food.route("/cat")
def cat():
    resp = {}
    req = request.values
    query = FoodCat.query

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(FoodCat.status == req['status'])

    data_list = query.order_by(FoodCat.weight.desc(), FoodCat.id.desc()).all()
    resp['list'] = data_list
    resp['status_mapping'] = app.config['STATUS_MAPPING']
    resp['search_con'] = req
    return ops_render("food/cat.html", resp)


@route_food.route("/cat-set", methods=['GET', 'POST'])
def cat_set():
    if request.method == 'GET':
        resp = {}
        req = request.args
        id = int(req.get('id', 0))
        info = None
        if id:
            info = FoodCat.query.filter_by(id=id).first()

        resp['info'] = info
        resp['current'] = 'cat'

        return ops_render("food/cat_set.html", resp)

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    print(req)
    id = req['id'] if 'id' in req else 0
    name = req['name'] if 'name' in req else ''
    weight = int(req['weight']) if 'weight' in req and int(req['weight']) > 0 else 1

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的分类名称~'
        return jsonify(resp)

    print(id)
    food_cat_info = FoodCat.query.filter_by(id=id).first()
    if food_cat_info:
        model_food_cat = food_cat_info
    else:
        model_food_cat = FoodCat()
        model_food_cat.created_time = getCurrenDate()
    model_food_cat.name = name
    model_food_cat.weight = weight
    model_food_cat.updated_time = getCurrenDate()
    db.session.add(model_food_cat)
    db.session.commit()
    return jsonify(resp)


@route_food.route("/cat-ops", methods=['POST'])
def cat_ops():
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

    food_info = FoodCat.query.filter_by(id=id).first()

    if not food_info:
        resp['code'] = -1
        resp['msg'] = '选项不存在~~'
        return jsonify(resp)

    if act == 'remove':
        food_info.status = 0
    elif act == 'recover':
        food_info.status = 1

    food_info.updated_time = getCurrenDate()
    db.session.add(food_info)
    db.session.commit()

    return jsonify(resp)
