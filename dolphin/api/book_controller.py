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
from dolphin.common.net.restful.api_response import CustomJsonResponse

logger = logging.getLogger(__name__)
producer = KafkaProducer(
  bootstrap_servers=['mq-server:9092'],
  api_version = (0,10,2,0) # solve no broker error
)

class BookController(APIView):

  parser_classes = (JSONParser,)

  def post(self,request):
    if isinstance(request.body, bytes):
      try:
          producer.send('dolphin-spider-google-book-bookinfo', request.body)
      except Exception as e:
        str_body = str(request.body, encoding='utf-8')
        logger.error("Save book encount an error: " + str_body,e)
        return CustomJsonResponse(data=e,code="50000",desc="saving book to kafka failed") 
    return CustomJsonResponse(data="Success",code="20000",desc="ok" )  

  def get(self,request):
    param_dict = request.query_params
    if isinstance(param_dict, QueryDict):
        param_dict = param_dict.dict()
    return JsonResponse(param_dict,safe=False)
