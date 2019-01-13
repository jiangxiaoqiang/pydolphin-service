# -*- coding: UTF-8 -*-

import json
import urllib
import logging
import demjson
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from dolphin.models.bookmodel import Book
from urllib import request, parse
from rest_framework.parsers import JSONParser
from django.http import QueryDict
from dolphin.models.bookserializer import BookSerializer
from dolphin.biz.doubanspiderbiz import doubanspiderbiz
from dolphin.db.ssdb_client import SsdbClient
from scrapy.utils.serialize import ScrapyJSONDecoder

logger = logging.getLogger(__name__)

class bookcontroller(APIView):

  parser_classes = (JSONParser,)

  def post(self,request):
    if isinstance(request.body, bytes):
      standard_json_object = {}
      try:
        str_body = str(request.body, encoding='utf-8')
        plan_json_text = urllib.parse.unquote_plus(str_body)
        _decoder = ScrapyJSONDecoder()
        standard_json_object = _decoder.decode(plan_json_text)
      except Exception as e:
        logger.error("Save book: " + str_body,e)
      return self.save_single_book(standard_json_object) 
    return JsonResponse("error", status=400,safe=False)
  
  def save_single_book(self,books):
    for key in books:
      single_book = books[key]
      serializer = BookSerializer(data=single_book)
      if serializer.is_valid():
        #json_text = json.dumps(single_book)
        SsdbClient.qpush_front(SsdbClient,single_book)
    return JsonResponse("Success", status=200,safe=False)

  def get(self,request):
    param_dict = request.query_params
    if isinstance(param_dict, QueryDict):
        param_dict = param_dict.dict()
    return JsonResponse(param_dict,safe=False)
