# coding=utf-8
import datetime

from flask import g, render_template


def ops_render(template, context=None):
    """
    统一渲染模板附加参数
    :param template: 模板文件
    :param context: 附加参数
    :return: 模板文件
    """

    if context is None:
        context = {}
    if 'current_user' in g:
        context['current_user'] = g.current_user

    return render_template(template, **context)


def iPagination(params):
    """
    返回分页对象
    :param params:
    :return:
    """
    import math

    ret = {
        "is_prev": 1,
        "is_next": 1,
        "from": 0,
        "end": 0,
        "current": 0,
        "total_pages": 0,
        "page_size": 0,
        "total": 0,
        "url": params['url']
    }

    total = int(params['total'])
    page_size = int(params['page_size'])
    page = int(params['page'])
    display = int(params['display'])
    total_pages = int(math.ceil(total / page_size))
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0

    semi = int(math.ceil(display / 2))

    if page - semi > 0:
        ret['from'] = page - semi
    else:
        ret['from'] = 1

    if page + semi <= total_pages:
        ret['end'] = page + semi
    else:
        ret['end'] = total_pages

    ret['current'] = page
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    ret['range'] = range(ret['from'], ret['end'] + 1)
    return ret


def getCurrenDate(datetime_format="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间格式化字符串
    :param datetime_format: 返回格式
    :return: 时间字符串
    """
    return datetime.datetime.now().strftime(datetime_format)


def getDictFilterField(db_model, select_filed, key_field, id_list):
    """
    根据某个字段获取一个dic
    """
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter_by(select_filed.in_(id_list))

    list = query.all()
    if not list:
        return ret

    for item in list:
        if not hasattr(item, key_field):
            break
        ret[getattr(item, key_field)] = item
    return ret
