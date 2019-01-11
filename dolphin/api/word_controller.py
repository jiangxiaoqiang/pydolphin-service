# -*- coding: UTF-8 -*-

import json
import urllib
import logging
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from dolphin.models.bookmodel import Book
from urllib import request, parse
from rest_framework.parsers import JSONParser
from django.http import QueryDict
from django.core import serializers
from dolphin.serilizer.word_serializer import WordSerializer
from dolphin.biz.doubanspiderbiz import doubanspiderbiz
from dolphin.common.net.restful.api_response import CustomJsonResponse

logger = logging.getLogger(__name__)

class WordController(APIView):

  parser_classes = (JSONParser,)  

  def get(self,request):
    serializer = WordSerializer()
    result = serializer.get()
    serializer1 = WordSerializer(result, many=True)
    #https://q1mi.github.io/Django-REST-framework-documentation/tutorial/1-serialization_zh/
    #response_data['message'] = serializers.serialize("json", result)
    return  CustomJsonResponse(data=serializer1.data, code="20000", desc='get word success' )
  
  def put(self,request):
    if isinstance(request.body, bytes):
      str_body = str(request.body, encoding='utf-8')
      plan_json_text = urllib.parse.unquote_plus(str_body)
      data = json.loads(plan_json_text)
      serializer = WordSerializer(data=data)
      if serializer.is_valid():
        serializer.updateStatus(data["id"],data["state"])        
        return CustomJsonResponse(data=serializer.data,code="20000", desc="Save success")
      else:
        errors = serializer.errors
        logger.error(errors)
        return CustomJsonResponse(data="error",code = "50000",desc="Save failed")

