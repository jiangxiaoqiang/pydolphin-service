from rest_framework import serializers
from dolphin.models.word_model import Word
from rest_framework.pagination import PageNumberPagination
from dolphin.models.scrapy_urls_pool_model import ScrapyUrlsPool

class SpiderUrlsSerializer(serializers.Serializer):                
    result = serializers.CharField(required=False)
    scrapy_url = serializers.CharField(required=False)
    scrapy_status = serializers.CharField(required=False)
    spider_name =  serializers.CharField(required=False)   

    def get(self):        
        url_result = ScrapyUrlsPool.objects.filter(scrapy_status=0)[:1]      
        return url_result

    def create(self, validated_data):
        return ScrapyUrlsPool.objects.create(**validated_data)

    def updateStatus(self, state,id):
        return ScrapyUrlsPool.objects.filter(id=id).update(scrapy_status=state)