# -*- coding: UTF-8 -*-
#encoding=utf-8

import sys
import json
import time
import urllib
import ssl
import string
import random
import gzip
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

class doubanspiderbizapi:
    def __init__(self):
        return

    def get_conn(self):
        global_conn = psycopg2.connect(
            database="dolphin",
            user="postgres",
            password="postgres",
            host=confighelper.getValue(self, 'global', 'ip'),
            port="5432")
        return global_conn

    def get_api_single_book_detail_info(self, url, id):
        single_book = book()
        try:
            headers = utils.getHttpHeader()
            #proxy_support = urllib.request.ProxyHandler({'https': 'localhost:8888'})
            #opener = urllib.request.build_opener(proxy_support)
            #urllib.request.install_opener(opener)
            req = urllib.request.Request(url)
            for key in headers:
                req.add_header(key, headers[key])
            source_code = urllib.request.urlopen(req).read()
            plain_text = gzip.GzipFile(fileobj=source_code)
            plain_text_decode = str(plain_text, 'utf-8')
            single_book = json.loads(plain_text_decode)
        except Exception as e:
            logger.error(e)
        return single_book

    def save_api_book_lists(self):
        randomNumber = doubanspiderbiz.get_douban_book_id(doubanspiderbiz)
        single_book_url = confighelper.getValue(
            self, 'global', 'douban_book_api_url') + str(randomNumber)
        logger.info("Scrap address:" + single_book_url)
        book = self.get_api_single_book_detail_info(single_book_url,
                                                    randomNumber)
        if book['isbn13'] is not None and book['isbn13'] != '':
            conn = self.get_conn()
            cur = conn.cursor()
            current_date = utils.GetNowTime()
            publisher = []
            publisher.append(book['publisher'])
            value = [
                book['title'], book['isbn13'], book['author'], publisher,
                book['pubdate'], book['binding'], book['price'], current_date,
                str(randomNumber), book['subtitle'], book['origin_title'], '',
                book['translator'], book['pages'], book['isbn10'],
                'douban-api-spider', book['summary']
            ]
            sql = "select count(*) from book where isbn=%s"
            isbn = str(book['isbn13'].strip())
            cur.execute(sql, [isbn])
            (count, ) = cur.fetchone()
            if count is None or count < 1:
                insert_sql = '''insert into book(name,
                isbn,
                author,
                publisher,
                publish_year,
                binding,price,
                add_date,
                douban_id,
                subtitle,
                original_name,
                issuer,
                translator,
                pages,
                isbn10,
                source,
                summary) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                cur.execute(insert_sql, value)
                doubanspiderbiz.update_douban_book_id(
                    doubanspiderbiz, randomNumber, 1,
                    '200,douban_id:' + str(randomNumber))
            else:
                # 书籍已经存在，直接更新记录
                doubanspiderbiz.update_douban_book_id(
                    doubanspiderbiz, randomNumber, 1, 'aready exits')
            conn.commit()
            cur.close()
            conn.close()
        else:
            doubanspiderbiz.update_douban_book_id(
                doubanspiderbiz, randomNumber, 1, 'isbn is null')
