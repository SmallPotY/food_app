# coding=utf-8
import hashlib, base64


class UserService():

    @staticmethod
    def geneAuthCode(user_info):
        """加密"""
        m = hashlib.md5()
        str = "{}-{}-{}-{}".format(user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd, salt):
        """解密"""
        m = hashlib.md5()
        str = "{}-{}".format(base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()
