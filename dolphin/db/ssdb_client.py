# -*- coding: UTF-8 -*-

import pyssdb
import logging
import json

#c = pyssdb.Client('127.0.0.1',8888)
c = ''

logger = logging.getLogger(__name__)

class SsdbClient:

    def __init__(self):
        return
    
    def set(self):
        try:
            c.set("book_queu1","item_value")
        except Exception as e:
            logger.error(e)

    def get(self):
        try:
            return c.get("book_queu1")
        except Exception as e:
            logger.error(e)

    def qpush_front(self,data):
        try:
            item_value = json.dumps(data)            
            c.qpush_front("book_queue",item_value)
        except Exception as e:
            logger.error(e)


    def qpop_back(self):
        try:
            pop_content = c.qpop_back("book_queue")
            return pop_content
        except Exception as e:
            logger.error(e)