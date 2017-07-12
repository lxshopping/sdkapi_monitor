#coding:utf8
import os
import config
import Crypt3DES
# from Crypto.Cipher import DES
import urllib, urllib2
import json
import time, datetime
import hashlib
import requests
import logging


'''
Readme:
pip install pycrypto

'''

class http_method(object):

    def __init__(self):
        pass

        # self.message = message


    def inform_post(self,mess_infom):
        # post的组接口
        # url = 'https://oapi.dingtalk.com/robot/send?access_token=6e7583cdcb89f266026a21723e52aedd63dd21e8aa2e2c061b35e734759cf920'
        url = 'https://oapi.dingtalk.com/robot/send?access_token=d57917a72fe6c56b545acb78a888d780a2a06ab835d0376ca225acc7dd7bf5dd'
        # payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}

        ret = requests.post(url, data=json.dumps(mess_infom), headers=headers)

        return ret.text
        # print ret.cookies


    def inform_get(self):

        pass

def infor_dd():

    dd_infor = http_method()

    with open('/tmp/message.dd', 'ab+') as write_file_dd:
        write_file_dd.seek(0)
        message_dd = write_file_dd.read()
        # message_dd.encode('utf-8')

        if len(message_dd) > 0:
            values = { "msgtype": "text","text": {"content": message_dd}, "at": {"atMobiles": ["18607169123","13986238346","18627051621","15021829660","18507554340"], } }
            dd_infor.inform_post(values)

        else:
            logging.info("接口正常:%s" % (message_dd))

    with open('/tmp/message.dd', 'w+') as write_file_dd:
        clear_file_dd = ''
        write_file_dd.write(clear_file_dd)

    # print "Sleep 14400s..."
    # time.sleep(14400)

def request(uri, **data):
    url = URL(uri);

    logging.info("\n============================================== %s" % (url))

    params = postdata(**data);

    # print params

    logging.info("request: %s\n" % (json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)))

    try:
        request = urllib2.Request(url, urllib.urlencode(params))
        response = urllib2.urlopen(request)
    except Exception as e:
        # 接口异常
        with open('/tmp/message.dd', 'ab+') as write_file_dd:
            write_file_dd.write('\nsdk接口异常:\n请检查接口:%s\n错误信息如下:\n%s\n' %(url,e) )

        # print "\033[1;31;40m%d,%s\033[0m" % (e.code, e.msg)
    else:
        res = response.read()
        try:
            data = json.loads(res)
        except Exception as e:
            # 接口返回参数异常
            with open('/tmp/message.dd', 'ab+') as write_file_dd:
                write_file_dd.write('\nsdk接口返回参数异常:\n请检查接口:%s\n返回结果:%s\n错误信息如下:\n%s\n' % (url,res,e))
            # print "response:%s" % (res)
            # print "\033[1;31;40m返回值无法解析\033[0m"
            # raw_input('按回车键继续 ...')
        else:
            # print "\033[0mresponse: %s" % (json.dumps(data['data'], indent=4, sort_keys=False, ensure_ascii=False))

            logging.info("response: %s" % (json.dumps(data['data'], indent=4, sort_keys=False, ensure_ascii=False)))

            if data["code"] != 1:
                # 代码逻辑问题
                with open('/tmp/message.dd', 'ab+') as write_file_dd:
                    write_file_dd.write('\nsdk接口代码逻辑异常:\n请检查接口:%s\n错误返回参数如下:\n%s\ncode:%d\n' % (url,data["msg"], data["code"]))
                # print "\033[1;31;40m%s(%d)\033[0m" % (data["msg"], data["code"])
                # raw_input('按回车键继续 ...')
            else:
                # print type(data["data"])
                return data["data"]
    infor_dd()
    return None

def postdata(**data):
    data['_appid'] = config.APPID
    data['_timestamp'] = int(time.mktime(datetime.datetime.now().timetuple()))
    data['_rid'] = config.RID
    data['_type'] = 'json'
    data['_sign_type'] = 'md5'
    if os.path.isfile('.uuid'):
        data['_device_id'] = open('.uuid').read()
    else:
        data['_device_id'] = ''

    datastr = ""
    for key in sorted(data.keys()):
        k = urllib.quote_plus(key)
        v = urllib.quote_plus(str(data[key]))

        datastr = datastr + "%s=%s&" % (k, v)

    md5 = hashlib.md5()
    md5.update(datastr + "key=" + config.APPKEY)
    
    data['_sign'] = md5.hexdigest()

    return data

def URL(uri):
    return config.BASEURL + uri

def __encrypt_param(data):
    data = urllib.urlencode(data)
    return Crypt3DES.encrypt(data, config.APPKEY)

