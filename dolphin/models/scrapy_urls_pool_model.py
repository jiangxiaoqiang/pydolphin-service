from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import FileField

class ScrapyUrlsPool(models.Model):
    id = models.CharField(blank=False,primary_key=True,max_length=18)
    scrapy_url = models.CharField(blank=False,max_length=1024)
    result = models.CharField(blank=False,max_length=256)
    scrapy_status = models.CharField(blank=False,max_length=4)
    spider_name = models.CharField(blank=False,max_length=256)
   
    class Meta:
        db_table = 'spider_urls_pool'