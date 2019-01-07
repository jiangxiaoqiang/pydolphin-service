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
from dolphin.models.bookserializer import BookSerializer
from dolphin.biz.doubanspiderbiz import doubanspiderbiz

logger = logging.getLogger(__name__)

class WordController(APIView):

  parser_classes = (JSONParser,)  

  def get(self,request):
    param_dict = request.query_params
    if isinstance(param_dict, QueryDict):
        param_dict = param_dict.dict()
    return JsonResponse(param_dict,safe=False)
