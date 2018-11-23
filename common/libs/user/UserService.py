# coding=utf-8
import hashlib, base64, random, string


class UserService():

    @staticmethod
    def geneAuthCode(user_info=None):
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

    @staticmethod
    def geneSalt(length=16):
        """生成随机字符串"""
        # key = [random.choice(string.ascii_uppercase + string.digits) for i in range(length)]
        key = random.sample(string.ascii_letters + string.digits, length)
        return "".join(key)


if __name__ == '__main__':
    print(UserService.geneSalt())
