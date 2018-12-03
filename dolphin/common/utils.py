#coding=utf-8

import urllib
import re
import time
import string
import random
import numpy

class utils:

    @staticmethod
    def GetNowTime():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        
    @staticmethod
    def getHttpHeader():
        items = string.ascii_letters + string.digits
        random_str=random.sample(items, 11)
        cookie = "bid=%s" % "".join(random_str)
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Cookie':cookie,
            'Accept-Encoding':'deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'Cache-Control':'max-age=0',
            'DNT':1
        }
        return headers
