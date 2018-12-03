# -*- coding: UTF-8 -*-

import json
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from dolphin.models.bookmodel import Book
from rest_framework.parsers import JSONParser
from dolphin.models.bookserializer import BookSerializer
from django.http import QueryDict

from dolphin.biz.doubanspiderbiz import doubanspiderbiz

class doubanbookcontroller(APIView):
  def get(self,request):
    douban_book_id = doubanspiderbiz.get_douban_book_id(doubanspiderbiz)
    return JsonResponse(douban_book_id,safe=False)
