# coding=utf-8
from werkzeug.utils import secure_filename
from application import app, db
from common.libs.Helper import getCurrenDate
import os
import stat
import uuid
from common.models.Images import Images


class UploadService:

    @staticmethod
    def upload_by_file(file):
        config_upload = app.config['UPLOAD']
        resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1]
        if ext not in config_upload['ext']:
            resp['code'] = -1
            resp['msg'] = '不允许的拓展类型文件'
            return resp

        root_path = app.root_path + config_upload['prefix_path']

        file_dir = getCurrenDate("%Y%m%d")
        save_dir = root_path + file_dir
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

        file_name = str(uuid.uuid4()).replace("-", "") + "." + ext
        file.save("{}/{}".format(save_dir, file_name))

        model_image = Images()
        model_image.file_key = file_dir + '/' + file_name
        model_image.created_time = getCurrenDate()
        db.session.add(model_image)
        db.session.commit()
        resp['data'] = {
            'file_key': model_image.file_key
        }
        return resp