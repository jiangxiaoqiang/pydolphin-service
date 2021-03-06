import time
from rest_framework import serializers
#from dolphin.serilizer.spider_urls_serializer import SpiderUrlsSerializer
from dolphin.models.word_model import Word
from rest_framework.pagination import PageNumberPagination
from dolphin.models.scrapy_urls_pool_model import ScrapyUrlsPool

class SpiderUrlsSerializer(serializers.Serializer):                
    result = serializers.CharField(required=False)
    scrapy_url = serializers.CharField(required=False)
    scrapy_status = serializers.CharField(required=False)
    spider_name =  serializers.CharField(required=False)
    update_date = serializers.DateTimeField(required=False)   

    def get(self,spider_name):        
        url_result = ScrapyUrlsPool.objects.filter(scrapy_status=0,spider_name=spider_name)[:1]
        #url_serializer = SpiderUrlsSerializer(url_result, many=True)
        #scrapy_url = url_serializer.data["scrapy_url"]
        #self.updateStatus(-1,scrapy_url)      
        return url_result

    def create(self, validated_data):
        return ScrapyUrlsPool.objects.create(**validated_data)

    def updateStatus(self, state,scrapy_url):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return ScrapyUrlsPool.objects.filter(scrapy_url=scrapy_url).update(scrapy_status=state,update_date=current_time)