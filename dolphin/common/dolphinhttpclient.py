# -*- coding: UTF-8 -*-
#encoding=utf-8

import sys
import json
import time
import urllib
import ssl
import string
import random
from bs4 import BeautifulSoup
from scrapy import Request
from urllib import request, parse
import psycopg2
from dolphin.book import book
import requests
import unicodedata
from dolphin.common.commonlogger import commonlogger
import numpy as numpy
import logging
from dolphin.biz.doubanparser import doubanparser
from dolphin.config.confighelper import confighelper
from dolphin.biz.doubanspiderbiz import doubanspiderbiz
from dolphin.common.utils import utils
from scrapy.utils.serialize import ScrapyJSONEncoder

ssl._create_default_https_context = ssl._create_unverified_context

logger = logging.getLogger(__name__)

class dolphinhttpclient:

    def __init__(self):
        return      

    def get(self,url):
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req).read()
        response_text = str(response,'utf-8')
        return response_text

    def get_response_data(self,url):          
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req).read()
        response_text = str(response,'utf-8')
        response_data = json.loads(response_text)
        return response_data

    def get_response_data_google(self,url):
        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)"}
        #req = request.Request("https://www.googleapis.com/books/v1/volumes?q=1", headers=headers)
        proxy_support = urllib.request.ProxyHandler({'https': '127.0.0.1:1080'})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        req = request.Request(url, headers=headers)
        #req = urllib.request.Request(url)
        response = urllib.request.urlopen(req).read()
        response_text = str(response,'utf-8')
        response_data = json.loads(response_text)
        return response_data

    def put(self,url,data):
        headers = {'Content-type': 'application/json'}
        str_data = json.dumps(dict(data[0]))
        encode_data = urllib.parse.quote_plus(str_data)
        data = bytes(encode_data,'utf8')
        req = urllib.request.Request(url=url,data = data,headers = headers,method='PUT')
        response = urllib.request.urlopen(req,data=data).read()
        response_text = str(response,'utf-8')
        response_data = json.loads(response_text)
        return response_data

    def post(self,url,data):
        response_text = ''
        try:
            #proxy_support = urllib.request.ProxyHandler({'http': 'localhost:8888'})
            #opener = urllib.request.build_opener(proxy_support)
            #urllib.request.install_opener(opener)
            #req = urllib.request.Request(url)
            headers = {'Content-type': 'application/json'}
            str_data = str(data)
            encode_data = urllib.parse.quote_plus(str_data)
            data = bytes(encode_data,'utf8')
            req = urllib.request.Request(url=url,data = data,headers = headers,method='POST')
            response = urllib.request.urlopen(req,data=data).read()
            response_text = str(response,'utf-8')
        except Exception as e:
            logger.error(e)
        return response_text

    def post_json(self,url,data):
        response_text = ''
        try:            
            headers = {'Content-type': 'application/json'}
            _encoder = ScrapyJSONEncoder()
            encode_result = _encoder.encode(data)
            encode_data_bytes = urllib.parse.quote_plus(encode_result)
            # convert bytes for network transfer
            data = bytes(encode_data_bytes,'utf8')
            req = urllib.request.Request(url=url,data = data,headers = headers,method='POST')
            response = urllib.request.urlopen(req).read()
            response_text = str(response,'utf-8')
        except Exception as e:
            logger.error("post json error,detail %s",e)
        return response_text

    
