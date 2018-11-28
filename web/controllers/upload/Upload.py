# coding=utf-8
from flask import Blueprint, request, jsonify
from application import app, db
import json, re
from common.libs.UploadService import UploadService

route_upload = Blueprint('upload_page', __name__)


@route_upload.route('ueditor', methods=['GET', 'POST'])
def ueditor():
    req = request.values

    action = req['action'] if 'action' in req else ''

    if action == 'config':
        root_path = app.root_path
        config_path = "{}\\web\\static\\plugins\\ueditor\\upload_config.json".format(root_path)
        with open(config_path, encoding='utf-8') as fp:
            try:
                config_data = json.loads(re.sub(r'\/\*.*\*/', '', fp.read()))
            except:
                config_data = {}
        return jsonify(config_data)

    if action == 'uploadimage':
        return upload_image()
    return 'ueditor'


def upload_image():
    resp = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': ''}

    file_target = request.files     # 获取上传文件
    upfile = file_target['upfile'] if 'upfile' in file_target else None

    if upfile is None:
        resp['state'] = '上传失败'
        return jsonify(resp)

    ret =UploadService

    return jsonify(resp)