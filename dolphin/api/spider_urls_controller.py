# -*- coding: UTF-8 -*-

from rest_framework.views import APIView
from dolphin.serilizer.spider_urls_serializer import SpiderUrlsSerializer
from dolphin.common.net.restful.api_response import CustomJsonResponse


class SpiderUrlsController(APIView):

    def get(self,request):
        serializer = SpiderUrlsSerializer()
        result = serializer.get()
        serializer_response = SpiderUrlsSerializer(result, many=True)
        return  CustomJsonResponse(data=serializer_response.data, code="20000", desc='ok' )


