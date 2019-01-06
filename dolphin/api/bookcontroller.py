# -*- coding: UTF-8 -*-

import json
import urllib
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from dolphin.models.bookmodel import Book
from urllib import request, parse
from rest_framework.parsers import JSONParser
from django.http import QueryDict
from dolphin.models.bookserializer import BookSerializer
from dolphin.biz.doubanspiderbiz import doubanspiderbiz
from dolphin.common.commonlogger import commonlogger

logger = commonlogger()
commonloggerinstance = commonlogger()
logger = commonloggerinstance.getlogger()

class bookcontroller(APIView):

  parser_classes = (JSONParser,)

  def post(self,request):
    if isinstance(request.body, bytes):
      str_body = str(request.body, encoding='utf-8')
      plan_json_text = urllib.parse.unquote_plus(str_body)
      data = json.loads(plan_json_text)
      serializer = BookSerializer(data=data)
      if serializer.is_valid():
        self.save_book(data,serializer)
        return JsonResponse(serializer.data, status=201)
      else:
        errors = serializer.errors
        logger.error(errors)

    return JsonResponse(serializer.errors, status=400)
  
  def save_book(self,data,serializer):
    douban_id = data["douban_id"]
    try:
      isbn13 = data["isbn"]
      sql = "select count(*) from book where isbn=%s"
      conn = doubanspiderbiz.get_conn(doubanspiderbiz)
      cur = conn.cursor()
      isbn = str(isbn13.strip())
      cur.execute(sql,[isbn])
      (count,) = cur.fetchone()
      if count is None or count < 1 :
        serializer.save()
        doubanspiderbiz.update_douban_book_id(doubanspiderbiz,douban_id, 1, '200,douban_id:' + str(douban_id))
      else:
        doubanspiderbiz.update_douban_book_id(doubanspiderbiz,douban_id, 1, 'aready exits')
    except Exception as e:
      doubanspiderbiz.update_douban_book_id(doubanspiderbiz,douban_id, -1, 'scrapy failed')
      logger.error(e)

  def get(self,request):
    param_dict = request.query_params
    if isinstance(param_dict, QueryDict):
        param_dict = param_dict.dict()
    return JsonResponse(param_dict,safe=False)
