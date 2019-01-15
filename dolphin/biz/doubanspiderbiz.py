# -*- coding: UTF-8 -*-
#encoding=utf-8

import sys
import time
import urllib
from bs4 import BeautifulSoup
import psycopg2
from dolphin.book import book
import requests
import unicodedata
from dolphin.common.commonlogger import commonlogger
import numpy as numpy
from dolphin.biz.doubanparser import doubanparser
from dolphin.config.confighelper import confighelper
from dolphin.common.utils import utils
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
logger = commonlogger()
type = sys.getfilesystemencoding()

commonloggerinstance = commonlogger()
logger = commonloggerinstance.getlogger()

class doubanspiderbiz:
    def __init__(self):
        return

    def get_conn(self):
        global_conn = psycopg2.connect(database="dolphin", 
                    user="postgres", 
                    password="postgres", 
                    host=confighelper.getValue(self,'global', 'ip'), 
                    port="5432")
        return global_conn

    def update_douban_book_id(self,id, isscrapy, result):
        try:
            sql = "select count(*) from spider_urls_pool where id=%s"
            conn = self.get_conn(self)
            cur = conn.cursor()
            cur.execute(sql,[id])
            (count,) = cur.fetchone()
            if (count == 1):
                self.update_douban_book_id_impl(id,isscrapy,result)
        except Exception as e:
            logger.error(e)

    def update_douban_book_id_impl(self,id, isscrapy, result):
        conn = self.get_conn(self)
        current_date = utils.GetNowTime()
        sql = '''
            update spider_urls_pool 
            set isscapy =%s,
                result =%s,
                update_date =%s 
            where id = %s
            '''
        cur = conn.cursor()
        cur.execute(sql,(str(isscrapy),result,current_date,str(id)))
        conn.commit()

    def get_single_book_detail_info(self,url, id):
        single_book = book()
        try:
            headers = utils.getHttpHeader()
            req = urllib.request.Request(
                url, headers=headers[numpy.random.randint(0, len(headers))])
            source_code = urllib.request.urlopen(req).read()
            plain_text = str(source_code,'utf-8')
            doubanparserinstance = doubanparser()
            single_book = doubanparserinstance.parseWebPage(plain_text)
        except Exception as e:
            logger.error(e)
        return single_book

    def save_book_lists(self):
        randomNumber = self.get_douban_book_id()
        single_book_url = 'https://book.douban.com/subject/' + str(randomNumber)
        logger.info(single_book_url)
        book = self.get_single_book_detail_info(single_book_url, randomNumber)
        if book.isbn != '':
            conn = self.get_conn()
            cur = conn.cursor()
            current_date = utils.GetNowTime()
            value = [book.name, 
                        book.isbn,
                        book.author , 
                        book.publisher , 
                        book.publish_year, 
                        book.binding,
                        book.pricing, 
                        current_date, 
                        str(randomNumber),
                        book.subtitle,
                        book.original_name,
                        book.issuer,
                        book.translator,
                        book.pages]
            sql = "select count(*) from book where isbn=%s"
            isbn = str(book.isbn.strip())
            cur.execute(sql,[isbn])
            (count,) = cur.fetchone()
            if count is None or count < 1 :
                insert_sql = '''insert into book(name,
                isbn,author,
                publisher,
                publish_year,
                binding,price,
                add_date,
                douban_id,
                subtitle,
                original_name,
                issuer,
                translator,
                pages) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                cur.execute(insert_sql,value)
                self.update_douban_book_id(randomNumber, 1, '200,douban_id:' + str(randomNumber))
            else:
                # 书籍已经存在，直接更新记录
                self.update_douban_book_id(randomNumber, 1, 'aready exits')
            conn.commit()
            cur.close()
            conn.close()
        else:
            self.update_douban_book_id(randomNumber, 1, 'isbn is null')

    def get_douban_book_id(self):
        conn = self.get_conn(self)
        sql = '''SELECT * 
                FROM douban_book_id 
                where isscapy = 0
                OFFSET floor(random()*8999999) 
                LIMIT 1'''
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            result_id = row[0]
        conn.commit()
        conn.close() 
        self.update_douban_book_id(self,result_id, -1, 'crawling...')
        return result_id

    def save_book(self,data,serializer):
        douban_id = data["douban_id"]
        try:
            isbn13 = data["isbn"]
            sql = "select count(*) from book where isbn=%s"
            conn = self.get_conn(self)
            cur = conn.cursor()
            isbn = str(isbn13.strip())
            cur.execute(sql,[isbn])
            (count,) = cur.fetchone()
            if count is None or count < 1 :
                if(serializer.is_valid()):
                    serializer.save()
                    self.update_douban_book_id(doubanspiderbiz,douban_id, 1, '200,douban_id:' + str(douban_id))
            else:
                self.update_douban_book_id(doubanspiderbiz,douban_id, 1, 'aready exits')
        except Exception as e:
            self.update_douban_book_id(doubanspiderbiz,douban_id, -1, 'scrapy failed')
            logger.error(e)
