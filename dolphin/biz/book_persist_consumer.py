# -*- coding: UTF-8 -*-

import logging
import time
import urllib
import json
import ast
from dolphin.db.ssdb_client import SsdbClient
from scrapy.utils.serialize import ScrapyJSONDecoder
from dolphin.biz.doubanspiderbiz import doubanspiderbiz
from dolphin.models.bookserializer import BookSerializer

logger = logging.getLogger(__name__)

# Invoke rest api to pull info from client
# Communication with restful service
class BookPersistConsumer():
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                comsumer_instance = BookPersistConsumer()
                comsumer_instance.save_book_to_db()
            except Exception as e:
                logger.error("book persist failed,detail info %s",e)
    
    def save_book_to_db(self):
        try:
            book_text_binary = SsdbClient.qpop_back(SsdbClient)
            if(book_text_binary is not None):            
                book_text_str = book_text_binary.decode("utf-8")
                book_object = ast.literal_eval(book_text_str)
                serializer = BookSerializer(data=book_object)
                doubanspiderbiz.save_book(doubanspiderbiz,book_object,serializer)
                logger.info("save book:" + book_text_str)
            else:
                logger.info("Having no book,sleep 30 sec...")
                time.sleep(30)
        except Exception as e:
            logger.error("save book to database failed, the detail : %s",e)






