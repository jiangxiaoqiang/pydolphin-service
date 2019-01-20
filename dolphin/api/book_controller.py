# -*- coding: UTF-8 -*-

import json
import urllib
import time
import logging
import demjson
import datetime
from django.http import HttpResponse, JsonResponse
from kafka import KafkaProducer
from rest_framework.views import APIView
from dolphin.models.bookmodel import Book
from urllib import request, parse
from rest_framework.parsers import JSONParser
from django.http import QueryDict
from dolphin.models.bookserializer import BookSerializer
from dolphin.serilizer.industry_identifiers_serializer import IndustryIdentifiersSerializer
from dolphin.biz.doubanspiderbiz import doubanspiderbiz
from dolphin.db.ssdb_client import SsdbClient
from scrapy.utils.serialize import ScrapyJSONDecoder

logger = logging.getLogger(__name__)
producer = KafkaProducer(
  bootstrap_servers=['mq-server:9092'],
  api_version = (0,10,2,0) # solve no broker error
)

class BookController(APIView):

  parser_classes = (JSONParser,)

  def post(self,request):
    if isinstance(request.body, bytes):
      standard_book_str = {}
      try:
          producer.send('dolphin-spider-google-book-bookinfo', request.body)
      except Exception as e:
        str_body = str(request.body, encoding='utf-8')
        logger.error("Save book encount an error: " + str_body,e)
      return self.save_single_book(standard_book_str) 
    return JsonResponse("error", status=400,safe=False)
  
  def save_single_book(self,books):   
    dict_type = type(books)
    if(dict_type == str and len(books) < 5):
      logger.warn("Null book info")
      return JsonResponse("Success", status=200,safe=False)
    if(books):
      starttime = datetime.datetime.now()
      for key in books:
        try:
          single_book = books[key]          
          single_book_str = json.dumps(single_book)
          single_book_bytes = str.encode(single_book_str)
          producer.send('dolphin-spider-google-book-bookinfo', single_book_bytes)
          logger.info("saving book info kafka...,detail: %s",single_book) 
        except Exception as e:
          logger.error("save book info kafka encount an error,detail %s ,book info: %s",e,books[key])
      endtime = datetime.datetime.now()
      logger.info('Saving kafka running time: %s Seconds',(endtime - starttime).seconds)
    return JsonResponse("Success", status=200,safe=False)

  def get(self,request):
    param_dict = request.query_params
    if isinstance(param_dict, QueryDict):
        param_dict = param_dict.dict()
    return JsonResponse(param_dict,safe=False)
