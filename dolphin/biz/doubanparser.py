# -*- coding: UTF-8 -*-

import sys
import time
import urllib
from bs4 import BeautifulSoup
import psycopg2
from unicodedata import normalize
from dolphin.book import book

class doubanparser:
    def parseWebPage(self,plain_text):
        soup = BeautifulSoup(plain_text,"html.parser")
        book1 = book()
        book1.publisher = []
        book1.author = []
        book1.translator = []
        book_name_object = soup.find('div', {'id': 'wrapper'}).find('h1')
        if book_name_object is not None:
            book1.name = book_name_object.text.strip()
        else:
            book1.name = ''
        list_info = soup.find('div', {'id': 'info'})
        if list_info is not None:
            list_soup = soup.find('div', {'id': 'info'}).findAll('span')
            if list_soup is not None and len(list_soup) > 0:
                for book_item in list_soup:
                    if type(book_item) != None:
                        if u'ISBN' in book_item.text:
                            book1.isbn = book_item.nextSibling.strip()
                        if u'作者' in book_item.text:
                            author = book_item.find('a')
                            if author is not None and author.text not in book1.author:
                                book1.author.append(author.text)
                        if u'出版社' in book_item.text:
                            if book_item.nextSibling is not None and book_item.nextSibling not in book1.publisher:
                                book1.publisher.append(book_item.nextSibling)
                        if u'出版年' in book_item.text:
                            book1.publish_year = book_item.nextSibling
                        if u'装帧' in book_item.text:
                            book1.binding = book_item.nextSibling
                        if u'定价' in book_item.text:
                            book1.pricing = book_item.nextSibling
                        if u'副标题' in book_item.text:
                            book1.subtitle = book_item.nextSibling
                        if u'原作名' in book_item.text:
                            book1.original_name = book_item.nextSibling
                        if u'译者' in book_item.text:
                            translator = book_item.parent.find('a')
                            if translator is not None and translator.text not in book1.translator:
                                book1.translator.append(translator.text)
                        if u'页数' in book_item.text:
                            book1.pages = book_item.nextSibling
        return book1
