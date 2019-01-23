# -*- coding: UTF-8 -*-

import time
import threading
import logging
import urllib
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from django.http import QueryDict
from django.forms.models import model_to_dict
from dolphin.models.scrapy_urls_pool_model import ScrapyUrlsPool
from dolphin.biz.book_persist_consumer import BookPersistConsumer
from dolphin.serilizer.spider_urls_serializer import SpiderUrlsSerializer
from dolphin.serilizer.word_serializer import WordSerializer
from dolphin.config.confighelper import confighelper
from dolphin.common.spiderconst import SpiderConst
from dolphin.common.dolphinhttpclient import dolphinhttpclient

logger = logging.getLogger(__name__)

class ConsumerController(APIView):
    def get(self,request):
        self.index(request)
        return JsonResponse("Book consumer deamon started",safe=False)

    def background_process(self):
        print("process started")
        bookPersistConsumer = BookPersistConsumer()
        bookPersistConsumer.run() 

    def google_url_generate_process(self):
        print("process url generate started")
        while(True):
            try:
                self.generate_imp()                
            except Exception as e:
                logger.error(e)
                        
    def generate_imp(self):
        wordSerializer = WordSerializer()
        result = wordSerializer.get()
        serializer1 = WordSerializer(result, many=True)            
        result_date = serializer1.data
        query_key_word = result_date[0]["word"]
        scrapy_urls = self.get_scrapy_urls(query_key_word)
        if(scrapy_urls):
            id = result_date[0]["id"]
            try:            
                for url in scrapy_urls:
                    self.persist_url(url)
                wordSerializer.updateStatus(1,id)
                logger.info("scrapy word:" + query_key_word + " complete!")
            except Exception as e:
                wordSerializer.updateStatus(-1,id)
                logger.error(e)

    def persist_url(self,url):        
        scrapy_url = ScrapyUrlsPool(spider_name="google-book-spider",
                                    scrapy_status = 0, 
                                    scrapy_url= url,
                                    result = "ready to scrapy")
        scrapy_url_dict = model_to_dict(scrapy_url)
        serializer = SpiderUrlsSerializer(data = scrapy_url_dict)
        valid = serializer.is_valid()
        error = serializer.errors
        if(valid):
            serializer.create(serializer.validated_data)        

    def get_scrapy_urls(self, query_key_word):
        startIndex = 0
        urls = []
        url_param = {
            "q": query_key_word,
            "maxResults": 40
        }
        url_main = confighelper.getValue(self, 'global', 'google_book_api_url')
        initial_url = url_main + "?" + urllib.parse.urlencode(url_param)
        total_elements = self.get_total_elements_num_by_keyword(
            initial_url)
        if(total_elements == 0):
            return urls
        while True:
            if(startIndex - 40 < total_elements):
                query_key_word_obj = {
                        "q": query_key_word
                }
                scrapy_param = urllib.parse.urlencode(query_key_word_obj) + "&maxResults="+ str(SpiderConst.GOOGLE_BOOK_DEFAULT_SCRAPY_SIZE) +"&startIndex=" + str(startIndex)
                scrapy_url = "?" + scrapy_param
                urls.append(scrapy_url)
                startIndex = startIndex + SpiderConst.GOOGLE_BOOK_DEFAULT_SCRAPY_SIZE
            else:
                break
        return urls

    def get_total_elements_num_by_keyword(self, initial_url):
        total_element = 0
        try:
            response_text = dolphinhttpclient.get_response_data_google(
                dolphinhttpclient, initial_url)
            if(response_text is not None):
                total_element = response_text["totalItems"]
        except Exception as e:
            logger.error("get google info encount an error,the detail %s",e)
        return total_element

    def index(self,request):
        t = threading.Thread(target=self.background_process, args=(), kwargs={})
        t.setDaemon(True)
        t.start() 
        param_dict = request.query_params
        if isinstance(param_dict, QueryDict):
            param_dict = param_dict.dict()
            is_generate_url = param_dict.get("is_generate_url")  
            if(is_generate_url == '1'):
                google_url_proc = threading.Thread(target=self.google_url_generate_process, args=(), kwargs={})
                google_url_proc.setDaemon(True)
                google_url_proc.start()
        return HttpResponse("main thread content")