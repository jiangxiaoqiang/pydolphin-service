# -*- coding: UTF-8 -*-

import json
import urllib
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from dolphin.models.bookmodel import Book
from urllib import request, parse
from rest_framework.parsers import JSONParser
from dolphin.models.bookserializer import BookSerializer
from django.http import QueryDict

class bookcontroller(APIView):

  parser_classes = (JSONParser,)

  def post(self,request):
    if isinstance(request.body, bytes):
      str_body = str(request.body, encoding='utf-8')

      plan_json_text = urllib.parse.unquote_plus(str_body)

      data = json.loads(plan_json_text)
      serializer = BookSerializer(data=data)
      if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
      else:
        errors = serializer.errors

    return JsonResponse(serializer.errors, status=400)
  
  def get(self,request):
    param_dict = request.query_params
    if isinstance(param_dict, QueryDict):
        param_dict = param_dict.dict()
    return JsonResponse(param_dict,safe=False)
