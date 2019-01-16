# -*- coding: UTF-8 -*-

import urllib
import json
import logging

from rest_framework.views import APIView
from django.http import QueryDict
from scrapy.utils.serialize import ScrapyJSONDecoder
from dolphin.serilizer.spider_urls_serializer import SpiderUrlsSerializer
from dolphin.common.net.restful.api_response import CustomJsonResponse

logger = logging.getLogger(__name__)

class SpiderUrlsController(APIView):

    def get(self,request):
        param_dict = request.query_params
        if isinstance(param_dict, QueryDict):
            param_dict = param_dict.dict()
            spider_name = param_dict.get("spider_name")
            serializer = SpiderUrlsSerializer()
            result = serializer.get(spider_name)
            serializer_response = SpiderUrlsSerializer(result, many=True)
        return  CustomJsonResponse(data=serializer_response.data, code="20000", desc='ok' )

    def put(self,request):
        if isinstance(request.body, bytes):
            str_body = str(request.body, encoding='utf-8')
            plan_json_text = urllib.parse.unquote_plus(str_body)
            try:
                _decoder = ScrapyJSONDecoder()
                standard_url_str = _decoder.decode(plan_json_text)
                serializer = SpiderUrlsSerializer(data=standard_url_str)
                if serializer.is_valid():
                    serializer.updateStatus(standard_url_str["scrapy_status"],standard_url_str["scrapy_url"])        
                    return CustomJsonResponse(data=serializer.data,code="20000", desc="Save success")
                else:
                    errors = serializer.errors
                    logger.error(errors)
                    return CustomJsonResponse(data="error",code = "50000",desc="Save failed")
            except Exception as e:
                logger.error(e)
                return CustomJsonResponse(data="error",code = "50000",desc= e)