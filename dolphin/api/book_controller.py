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
        str_body = str(request.body, encoding='utf-8')
        plan_json_text = urllib.parse.unquote_plus(str_body)
        _decoder = ScrapyJSONDecoder()
        standard_book_str = _decoder.decode(plan_json_text)
      except Exception as e:
        logger.error("Save book: " + str_body,e)
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
          bookSerializer = BookSerializer(data = single_book) 
          saved_book = bookSerializer.create(single_book)
          industryIdentifiers = single_book["industry_identifiers"]
          logger.info("saving book info...,detail: %s",single_book)          
          #producer.send("spider-google-book-bookinfo",single_book)
          producer.send("dolphin-test".encode('utf-8'),b"dolphin-client")
          self.save_identifiers_info(industryIdentifiers,saved_book.id)
        except Exception as e:
          logger.error("save book encount an error,detail %s ,book info: %s",e,books[key])
      endtime = datetime.datetime.now()
      logger.info('Running time: %s Seconds',(endtime - starttime).seconds)
    return JsonResponse("Success", status=200,safe=False)

  def save_identifiers_info(self,identifiers,book_id):
    if(identifiers):
      for identify in identifiers:        
        industryIdentifiersSerializer = IndustryIdentifiersSerializer(data = identify)
        identify["book_id"] = book_id
        is_valid = industryIdentifiersSerializer.is_valid()
        if(is_valid):
          producer.send("spider-google-book-identifiersinfo",identify)
          industryIdentifiersSerializer.save()
        

  def get(self,request):
    param_dict = request.query_params
    if isinstance(param_dict, QueryDict):
        param_dict = param_dict.dict()
    return JsonResponse(param_dict,safe=False)
