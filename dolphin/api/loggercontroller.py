# -*- coding: UTF-8 -*-

import json
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from dolphin.models.bookmodel import Book
from rest_framework.parsers import JSONParser
from dolphin.models.bookserializer import BookSerializer
from django.http import QueryDict
from kafka import KafkaProducer
from kafka.errors import KafkaError
from dolphin.common.commonlogger import commonlogger

commonloggerinstance = commonlogger()
logger = commonloggerinstance.getlogger()

class loggercontroller(APIView):
  def post(self,request):
    producer = KafkaProducer(bootstrap_servers=['broker1:1234'])
    topic = request.data["topic"]
    future = producer.send(topic, b'raw_bytes')
    try:
         future.get(timeout=10)
    except KafkaError:
      logger.error("write failed" + KafkaError)
    return JsonResponse("sucess",safe=False)
