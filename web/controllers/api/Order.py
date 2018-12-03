# -*- coding:utf-8 -*-
from flask import jsonify, request, g

from common.libs.UrlManager import UrlManager
from web.controllers.api import route_api
from common.models.food.Food import Food
import json
import decimal


@route_api.route('/order/info', methods=['POST'])
def order_info():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}

    req = request.values
    params_goods = req['goods'] if 'goods' in req else None
    member_info = g.member_info
    params_goods_list = []

    if params_goods:
        params_goods_list = json.loads(params_goods)

    food_dic = {}
    for item in params_goods_list:
        food_dic[item['id']] = item['number']

    food_ids = food_dic.keys()
    food_list = Food.query.filter(Food.id.in_(food_ids)).all()
    data_food_list = []
    yun_price = pay_price = decimal.Decimal(0.00)
    if food_list:
        for item in food_list:
            temp_data = {
                "id": item.id,
                "name": item.name,
                "price": str(item.price),
                "pic_url": UrlManager.build_image_url(item.main_iamge),
                'number': food_dic[item['id']]
            }
            pay_price = pay_price + item.price * int(food_dic[item.id])
            data_food_list.append(temp_data)

    default_address = {
        "name": "smallpot",
        "mobile": "18575757575",
        "address": "广东省广州市天河区"
    }

    resp['data']['food_list'] = data_food_list
    resp['data']['pay_price'] = str(pay_price)
    resp['data']['yun_price'] = str(yun_price)
    resp['data']['total_price'] = str(pay_price + yun_price)
    resp['data']['default_address'] = default_address
    return jsonify(resp)
