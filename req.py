#coding:utf8
import os,sys
import md5
import urllib, urllib2
import json
import random
import time
import getopt
import Http
import config
import uuid
import base64

reload(sys)
sys.setdefaultencoding('utf8')

def mobile(default = None):
    if default == None:
        return "156%s" % (str(random.random())[2:10])
    return default

def openid(default = None):
    if default == None:
        return str(uuid.uuid1())
    return default

def pause(type):
    if type >= 1:
        sys.exit(0)

#######################################################################################################################
"""
data = Http.request('api/account/username')
if data == None:
    sys.exit(0)

data = Http.request('api/account/register', username = data['username'], password = 123456)
if data == None:
    sys.exit(0)
    

TOKEN = data['token'];

data = Http.request('api/pay/order/new', _token = TOKEN, fee = 10, body = '10 Gold', subject = '10 Gold', notify_url = 'http://www.baidu.com/', vorderid = str(random.random())[2:], zone_id = 1, zone_name = "龙争虎斗", role_level = 1, role_name = "疯狂科学家", role_id = 10001)
if data == None:
    sys.exit(0)

ORDER_ID = data['order_id'];

Http.request('api/pay/mycard/payitem_query', _token = TOKEN);
sys.exit(0)
"""
####################################################################################################################### 后台工具：包查询

Http.request('api/tool/procedure/query', pname = '非常三国', rid = '3496')

####################################################################################################################### 后台工具：冻结
data = Http.request('api/account/username')
if data == None:
    sys.exit(0)

USERNAME = data['username']

data = Http.request('api/account/register', username = USERNAME, password = 123456)
if data == None:
    sys.exit(0)

Http.request('api/user/report_role', _token = data['token'], zone_id = 1, zone_name = "龙争虎斗", role_level = 1, role_name = "疯狂科学家", role_id = 10001)

Http.request('api/tool/user/freeze', ucid = data['uid'], status = 1, admin_user = 'lixx', comment = '使用外挂');
Http.request('api/account/login', username = USERNAME, password = 123456)
####################################################################################################################### 后台工具：解冻
Http.request('api/tool/user/freeze', ucid = data['uid'], status = 0, admin_user = 'lixx', comment = '解封');
Http.request('api/account/login', username = USERNAME, password = 123456)
####################################################################################################################### 后台工具：重设密码
data = Http.request('api/tool/user/reset_password_page', ucid = data['uid']);
Http.request('api/tool/reset_password/request', token = data['token'], password = 123789);
####################################################################################################################### 后台工具：获取自设密码的连接
"""
data = Http.request('api/account/username')
if data == None:
    sys.exit(0)

USERNAME = data['username']

Http.request('api/tool/user/reset_password_page', ucid = data['uid']);
pause(0)
"""
####################################################################################################################### 获取一个设备唯一ID

data = Http.request('api/app/uuid')
if data != None:
    open('.uuid', 'w').write(data['uuid'])

####################################################################################################################### 初始化

Http.request('api/app/initialize', app_version = '2.5', _imei = (str(random.random())[2:]), device_apps = '[{"AppName":"MD5签名生成器","PackageName":"com.sina.weibo.sdk.gensign","InstallTime":"1491389027713","UpdateTime":"1491389027713","VersionName":"1.0","VersionCode":"1"},{"AppName":"交管12123","PackageName":"com.tmri.app.main","InstallTime":"1488504181245","UpdateTime":"1488724951238","VersionName":"1.4.0","VersionCode":"10400"}]', device_info = '{"PhoneBrand":"Huawei","PhoneModel":"H60-L02","PhoneVersionName":"6.0","PhoneVersionCode":23,"PhoneIMEI":"864103021832966","PhoneIMSI":"460012679802931","PhoneNumber":"17092671941","PhoneScreen":"1080x1812"}')

####################################################################################################################### 退出客户端

Http.request('api/app/logout')

####################################################################################################################### 游客登陆

Http.request('api/account/guest/login')

####################################################################################################################### 找回密码（通过手机验证码）

MOBILE = mobile()
Http.request('api/account/mobile/login', mobile = MOBILE, code = 123456)
Http.request('api/account/user/sms_reset_password', mobile = MOBILE)
Http.request('api/account/user/reset_password', mobile = MOBILE, code = 123456, password = 123789)

####################################################################################################################### 一键登陆

data = Http.request('api/account/onekey/sms_token')
if data == None:
    sys.exit(0)

SMS_TOKEN = data['sms_token']
# ----------- 云片短信回调 -----------
data = {
    "base_extend": "8888",
    "extend": "01",
    "id": "2a70c6bb4f2845da816ea1bfe5732747",
    "mobile": mobile(),
    "reply_time": "2014-03-17 22:55:21",
    "text": SMS_TOKEN,
}
print Http.URL('callback/yunpian/request')
s = ''
key = ['base_extend', 'extend', 'id', 'mobile', 'reply_time', 'text']
for k in ['base_extend', 'extend', 'id', 'mobile', 'reply_time', 'text']:
    s = s + data[k] + ','
s = s + '560ff300cabf7b7df7e3c02f892bfd43'
m = md5.new()
m.update(s)
data['_sign'] = m.hexdigest()
req = urllib2.Request(Http.URL('callback/yunpian/request'), urllib.urlencode({"sms_reply": json.dumps(data)}))
print "\nbody:", urllib2.urlopen(req).read()
# ----------- 一键登陆轮询 -----------
Http.request('api/account/onekey/login', sms_token = SMS_TOKEN)

####################################################################################################################### 发送手机验证码、手机验证码登陆

MOBILE = mobile()

data = Http.request('api/account/mobile/sms_login', mobile = MOBILE)
if data == None:
    sys.exit(0)

Http.request('api/account/mobile/login', mobile = MOBILE, code = 123456)

####################################################################################################################### 自动登陆

data = Http.request('api/account/username')
if data == None:
    sys.exit(0)

USERNAME = data['username']

data = Http.request('api/account/register', username = USERNAME, password = 123456)
if data == None:
    sys.exit(0)

open('.token', 'w').write(data['token'])

Http.request('api/account/token/login', _token = open('.token').read())

####################################################################################################################### 第三方登陆

OPENID = openid()

Http.request('api/account/oauth/login', openid = openid(), unionid = openid(), type = 'weixin')

####################################################################################################################### 第三方登注册

OPENID = openid()

Http.request('api/account/oauth/register', openid = OPENID, unionid = OPENID, type = 'weixin', nickname = 'lixx', avatar = 'https://ss0.bdstatic.com/5.png')
Http.request('api/account/oauth/login', openid = OPENID, unionid = OPENID, type = 'weixin')

####################################################################################################################### 生成用户名、用户名注册

data = Http.request('api/account/username')
if data == None:
    sys.exit(0)

USERNAME = data['username']

data = Http.request('api/account/register', username = data['username'], password = 123456)
if data == None:
    sys.exit(0)

TOKEN = data['token'];

####################################################################################################################### 上传头像

Http.request('api/user/set_avatar', _token = TOKEN, type = 'bindata', avatar = base64.b64encode(open('avatar.png', 'rb').read()))

Http.request('api/user/set', _token = TOKEN, nickname = 'lixx', birthday = '19891212', province = '湖北省', city = '十堰市', address = '丹江口市丁家营镇4组38号')

####################################################################################################################### 设置用户名

Http.request('api/user/set_username', _token = TOKEN, username = 'lixx%s' % (str(random.random())[2:]))

####################################################################################################################### 设置昵称

Http.request('api/user/set_nickname', _token = TOKEN, nickname = 'lixx')

####################################################################################################################### 用户名或手机号码登陆

data = Http.request('api/account/username')
if data == None:
    sys.exit(0)

USERNAME = data['username']

Http.request('api/account/register', username = USERNAME, password = 123456)
Http.request('api/account/login', username = USERNAME, password = 123456)

####################################################################################################################### 实名认证

data = Http.request('api/account/username')
if data == None:
    sys.exit(0)

USERNAME = data['username']

data = Http.request('api/account/register', username = USERNAME, password = 123456)
if data == None:
    sys.exit(0)
    
TOKEN = data['token']

Http.request('api/user/attest', _token = TOKEN, name = 'lixx', card_id = '420381198908192719')

####################################################################################################################### 绑定手机

data = Http.request('api/account/username')
if data == None:
    sys.exit(0)

USERNAME = data['username']

data = Http.request('api/account/register', username = USERNAME, password = 123456)
if data == None:
    sys.exit(0)
    
TOKEN = data['token']
MOBILE = mobile()

data = Http.request('api/user/sms_bind_phone', _token = TOKEN, mobile = MOBILE)
if data == None:
    sys.exit(0)

Http.request('api/user/bind_phone', _token = TOKEN, mobile = MOBILE, code = 123456)

####################################################################################################################### 绑定平台账号

data = Http.request('api/account/username')
if data == None:
    sys.exit(0)

USERNAME = data['username']

data = Http.request('api/account/register', username = USERNAME, password = 123456)
if data == None:
    sys.exit(0)
    
TOKEN = data['token']

Http.request('api/user/bind_oauth', _token = TOKEN, openid = openid(), unionid = openid(), type = 'weixin', nickname = 'lixx', avatar = 'https://ss0.bdstatic.com/5.png')
Http.request('api/user/bind_list', _token = TOKEN)
Http.request('api/user/unbind_oauth', _token = TOKEN, type = 'weixin')

####################################################################################################################### 重设密码（通过旧密码）

data = Http.request('api/account/username')
if data == None:
    sys.exit(0)

data = Http.request('api/account/register', username = data['username'], password = 111111)
if data == None:
    sys.exit(0)
    
TOKEN = data['token']

Http.request('api/user/by_oldpassword_reset', _token = TOKEN, old_password = 111111, new_password = 123789)

####################################################################################################################### 重设密码（通过手机）

data = Http.request('api/account/mobile/login', mobile = mobile(), code = 123456)
if data == None:
    sys.exit(0)
    
TOKEN = data['token']

data = Http.request('api/user/sms_phone_reset_password', _token = TOKEN)
if data == None:
    sys.exit(0)

Http.request('api/user/phone_reset_password', _token = TOKEN, password = 123456, code = 888888)

####################################################################################################################### 解绑手机

MOBILE = mobile()
data = Http.request('api/account/mobile/login', mobile = mobile(), code = 123456)
if data == None:
    sys.exit(0)

TOKEN = data['token']

Http.request('api/user/sms_unbind_phone', _token = TOKEN)
Http.request('api/user/unbind_phone', _token = TOKEN, code = 123456)

data = Http.request('api/account/mobile/login', mobile = mobile(), code = 123456)
if data == None:
    sys.exit(0)

TOKEN = data['token']
####################################################################################################################### 新增小号

Http.request('api/user_sub/new', _token = TOKEN)
Http.request('api/user_sub/new', _token = TOKEN)
Http.request('api/user_sub/new', _token = TOKEN)

####################################################################################################################### 小号列表

data = Http.request('api/user_sub/list', _token = TOKEN)
if data == None:
    sys.exit(0)

####################################################################################################################### 修改小号昵称

Http.request('api/user_sub/set_nickname', _token = TOKEN, id = data['data'][0]['id'], nickname = str(random.random())[2:10]);

####################################################################################################################### 游戏小号

Http.request('api/user_sub/game_list', _token = TOKEN);

####################################################################################################################### 切换小号

data = Http.request('api/account/token/login', user_sub_id = data['data'][0]['id'], _token = TOKEN)
if data == None:
    sys.exit(0)

TOKEN = data['token']

####################################################################################################################### 上报角色信息

Http.request('api/user/report_role', _token = TOKEN, zone_id = 1, zone_name = "龙争虎斗", role_level = 1, role_name = "疯狂科学家", role_id = 10001)
Http.request('api/user/report_role', _token = TOKEN, zone_id = 1, zone_name = "龙争虎斗", role_level = 2, role_name = "疯狂科学家", role_id = 10001)
Http.request('api/user/report_role', _token = TOKEN, zone_id = 1, zone_name = "龙争虎斗", role_level = 3, role_name = "疯狂科学家", role_id = 10001)
Http.request('api/user/report_role', _token = TOKEN, zone_id = 1, zone_name = "龙争虎斗", role_level = 4, role_name = "疯狂科学家", role_id = 10001)
Http.request('api/user/report_role', _token = TOKEN, zone_id = 1, zone_name = "龙争虎斗", role_level = 5, role_name = "疯狂科学家", role_id = 10002)
Http.request('api/user/report_role', _token = TOKEN, zone_id = 1, zone_name = "龙争虎斗", role_level = 6, role_name = "疯狂科学家", role_id = 10003)

####################################################################################################################### 获取用户余额

Http.request('api/user/balance', _token = TOKEN)

####################################################################################################################### 创建购买F币的订单

data = Http.request('api/pay/order/f/new', _token = TOKEN, fee = 10, body = '10 Gold', subject = '10 Gold', zone_id = 1, zone_name = "龙争虎斗", role_level = 1, role_name = "疯狂科学家", role_id = 10001)

####################################################################################################################### 微信支付
data = Http.request('api/pay/order/new', _token = TOKEN, fee = 10, body = '10 Gold', subject = '10 Gold', notify_url = 'http://www.baidu.com/', vorderid = str(random.random())[2:], zone_id = 1, zone_name = "龙争虎斗", role_level = 1, role_name = "疯狂科学家", role_id = 10001)
if data == None:
    sys.exit(0)

ORDER_ID = data['order_id'];

Http.request('api/pay/nowpay_wechat/request', _token = TOKEN, order_id = ORDER_ID, balance = 0)

####################################################################################################################### 支付宝支付

data = Http.request('api/pay/order/new', _token = TOKEN, fee = 10, body = '10 Gold', subject = '10 Gold', notify_url = 'http://www.baidu.com/', vorderid = str(random.random())[2:], zone_id = 1, zone_name = "龙争虎斗", role_level = 1, role_name = "疯狂科学家", role_id = 10001)
if data == None:
    sys.exit(0)

ORDER_ID = data['order_id'];

Http.request('api/pay/alipay/request', _token = TOKEN, order_id = ORDER_ID, balance = 0);

####################################################################################################################### 银联支付

data = Http.request('api/pay/order/new', _token = TOKEN, fee = 10, body = '10 Gold', subject = '10 Gold', notify_url = 'http://www.baidu.com/', vorderid = str(random.random())[2:], zone_id = 1, zone_name = "龙争虎斗", role_level = 1, role_name = "疯狂科学家", role_id = 10001)
if data == None:
    sys.exit(0)

ORDER_ID = data['order_id'];

Http.request('api/pay/unionpay/request', _token = TOKEN, order_id = ORDER_ID, balance = 0);

####################################################################################################################### mycard支付

data = Http.request('api/pay/order/new', _token = TOKEN, fee = 10, body = '10 Gold', subject = '10 Gold', notify_url = 'http://www.baidu.com/', vorderid = str(random.random())[2:], zone_id = 1, zone_name = "龙争虎斗", role_level = 1, role_name = "疯狂科学家", role_id = 10001)
if data == None:
    sys.exit(0)

ORDER_ID = data['order_id'];

Http.request('api/pay/mycard/request', _token = TOKEN, order_id = ORDER_ID, balance = 0);

####################################################################################################################### 订单状态

Http.request('api/pay/order/info', _token = TOKEN, order_id = ORDER_ID);

####################################################################################################################### 充值记录

Http.request('api/user/recharge', _token = TOKEN);

####################################################################################################################### 消费记录

Http.request('api/user/consume', _token = TOKEN);

####################################################################################################################### 用户信息

Http.request('api/user/info', _token = TOKEN);

####################################################################################################################### 用户信息

Http.request('api/user/event', _token = TOKEN, event = 'download_app', data = '{}');

####################################################################################################################### 隐藏订单

Http.request('api/user/hide_order', _token = TOKEN, order_id = ORDER_ID);