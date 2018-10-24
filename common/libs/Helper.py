# coding=utf-8
from flask import g, render_template



def ops_render(template):
    """统一渲染方法,改写render_template,附加g变量"""
    context={}
    if 'current_user' in g:
        context['current_user'] = g.current_user

    return render_template(template,**context)
