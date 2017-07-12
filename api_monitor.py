#!/usr/bin/env python
# --*-- coding:utf-8 --*--

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
import logging
from logging.handlers import RotatingFileHandler

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




####################################################################################################################### 后台工具：冻结
'''
data = Http.request('api/account/username', )
if data == None:
    sys.exit(0)

USERNAME = data['username']

# data = Http.request('api/account/register', username = USERNAME, password = 123456)
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

'''




if __name__ == '__main__':

    # Rthandler = RotatingFileHandler('sdkapi_script.log', maxBytes=500*1024*1024,backupCount=5)
    # Rthandler.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # Rthandler.setFormatter(formatter)
    # logging.getLogger('').addHandler(Rthandler)

    logging.basicConfig(
        level=logging.DEBUG,
        format   = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
        datefmt  = '%Y-%m-%d %A %H:%M:%S',
        filename='sdkapi_script.log',
        # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        # datefmt='%a, %d %b %Y %H:%M:%S',
        filemode='w')


    console = RotatingFileHandler('sdkapi_script.log', maxBytes=500*1024*1024,backupCount=5)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)


    while True:

        #用户登录,获取token
        data = Http.request('api/account/login', username = 'lx123lx', password = 'lx123lx')

        try:
            TOKEN = data['token']
        #测试重要接口
            data = Http.request('api/pay/order/new', _token = TOKEN, fee = 10, body = '10 Gold', subject = '10 Gold', notify_url = 'http://www.baidu.com/', vorderid = str(random.random())[2:], zone_id = 1, zone_name = "龙争虎斗", role_level = 1, role_name = "疯狂科学家", role_id = 10001)
            if data == None:
                sys.exit(0)

            ORDER_ID = data['order_id']

            Http.request('api/pay/nowpay_wechat/request', _token = TOKEN, order_id = ORDER_ID, balance = 0)

            Http.request('api/user/info', _token = TOKEN)
        except Exception as e:
            logging.info("监控程序异常:%s" % (e))

        print "Sleep 120s..."
        time.sleep(120)













