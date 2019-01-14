# -*- coding: UTF-8 -*-

import urllib
import json
import logging

from rest_framework.views import APIView
from dolphin.serilizer.spider_urls_serializer import SpiderUrlsSerializer
from dolphin.common.net.restful.api_response import CustomJsonResponse

logger = logging.getLogger(__name__)

class SpiderUrlsController(APIView):

    def get(self,request):
        serializer = SpiderUrlsSerializer()
        result = serializer.get()
        serializer_response = SpiderUrlsSerializer(result, many=True)
        return  CustomJsonResponse(data=serializer_response.data, code="20000", desc='ok' )

    def put(self,request):
        if isinstance(request.body, bytes):
            str_body = str(request.body, encoding='utf-8')
            plan_json_text = urllib.parse.unquote_plus(str_body)
            data = json.loads(plan_json_text)
            serializer = SpiderUrlsSerializer(data=data)
            if serializer.is_valid():
                serializer.updateStatus(data["id"],data["scrapy_state"])        
                return CustomJsonResponse(data=serializer.data,code="20000", desc="Save success")
            else:
                errors = serializer.errors
                logger.error(errors)
                return CustomJsonResponse(data="error",code = "50000",desc="Save failed")
