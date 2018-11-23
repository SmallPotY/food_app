# coding=utf-8
import hashlib, base64, random, string,requests,json
from application import app

class MemberService():

    @staticmethod
    def geneAuthCode(member_info):
        """加密"""
        m = hashlib.md5()
        str = "{}-{}-{}".format(member_info.id,member_info.salt,member_info.status )
        m.update(str.encode("utf-8"))
        return m.hexdigest()


    @staticmethod
    def geneSalt(length=16):
        """生成随机字符串"""
        # key = [random.choice(string.ascii_uppercase + string.digits) for i in range(length)]
        key = random.sample(string.ascii_letters + string.digits, length)
        return "".join(key)


    @staticmethod
    def getWeChatOpenId(code):
        """获取微信的openid"""
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={appkey}&js_code={code}&grant_type=authorization_code".format(
            appid=app.config['MINA_APP']['AppID'], appkey=app.config['MINA_APP']['AppKey'], code=code)

        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid


if __name__ == '__main__':
    print(MemberService.geneSalt())
