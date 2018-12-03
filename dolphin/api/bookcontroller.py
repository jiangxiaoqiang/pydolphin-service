# -*- coding: UTF-8 -*-

import json
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from dolphin.models.bookmodel import Book
from rest_framework.parsers import JSONParser
from dolphin.models.bookserializer import BookSerializer
from django.http import QueryDict

class bookcontroller(APIView):
  def post(self,request):
    data_dumps = json.dumps(request.data)
    data = json.loads(data_dumps)
    serializer = BookSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
  
  def get(self,request):
    param_dict = request.query_params
    if isinstance(param_dict, QueryDict):
        param_dict = param_dict.dict()
    return JsonResponse(param_dict,safe=False)
