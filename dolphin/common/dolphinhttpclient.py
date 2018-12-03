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
import psycopg2
from dolphin.book import book
import requests
import unicodedata
from dolphin.common.commonlogger import commonlogger
import numpy as numpy
from dolphin.biz.doubanparser import doubanparser
from dolphin.config.confighelper import confighelper
from dolphin.biz.doubanspiderbiz import doubanspiderbiz
from dolphin.common.utils import utils

ssl._create_default_https_context = ssl._create_unverified_context
logger = commonlogger()
type = sys.getfilesystemencoding()

commonloggerinstance = commonlogger()
logger = commonloggerinstance.getlogger()

class dolphinhttpclient:
    def __init__(self):
        return      

    def get(self,url):
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req).read()
        response_text = str(response,'utf-8')
        return response_text

    def post(self,url,data):
        data = data.encode('utf8')
        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req).read()
        response_text = str(response,'utf-8')
        return response_text

    
