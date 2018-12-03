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
from dolphin.common.dolphinhttpclient import dolphinhttpclient

ssl._create_default_https_context = ssl._create_unverified_context
logger = commonlogger()
type = sys.getfilesystemencoding()

commonloggerinstance = commonlogger()
logger = commonloggerinstance.getlogger()

class doubanspiderbizapirest:
    def __init__(self):
        return    

    def get_api_single_book_detail_info(self, url, id):
        single_book = book()
        try:
            headers = utils.getHttpHeader()
            req = urllib.request.Request(url)
            for key in headers:
                req.add_header(key, headers[key])
            source_code = urllib.request.urlopen(req).read()
            plain_text = str(source_code, 'utf-8')
            single_book = json.loads(plain_text)
        except Exception as e:
            logger.error(e)
        return single_book   

    def get_douban_book_id_by_restservice(self):
        url = confighelper.getValue(self, 'global', 'rest_service_address') + "/spider/api/doubanbook"
        return dolphinhttpclient.get(dolphinhttpclient,url)

    def save_douban_book_by_restservice(self,book):
        url = confighelper.getValue(self,'global','rest_service_address') + "/spider/api/book"
        return dolphinhttpclient.post(dolphinhttpclient,url,book) 

    def save_rest_api_book_lists(self):
        random_book_id = doubanspiderbizapirest.get_douban_book_id_by_restservice(self)
        single_book_url = confighelper.getValue(self, 'global', 'douban_book_api_url') + str(random_book_id)
        logger.info("Scrap address:" + single_book_url)
        book = self.get_api_single_book_detail_info(single_book_url,random_book_id)
        if book['isbn13'] is not None and book['isbn13'] != '':
            book.creator = confighelper.getGloabalValue(self,'spider_man')
            current_date = utils.GetNowTime()
            publisher = []
            publisher.append(book['publisher'])
            value = [
                book['title'], book['isbn13'], book['author'], publisher,
                book['pubdate'], book['binding'], book['price'], current_date,
                str(random_book_id), book['subtitle'], book['origin_title'], '',
                book['translator'], book['pages'], book['isbn10'],
                'douban-api-spider', book['summary'],book['creator']
            ]
            self.save_douban_book_by_restservice(self,value)            
        else:
            logger.error("isbn13 is null")
