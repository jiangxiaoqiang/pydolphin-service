from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import FileField

class Word(models.Model):
    id = models.CharField(blank=False,max_length=256)
    word = models.CharField(blank=False,max_length=16)
    remark = models.CharField(blank=False,max_length=256)
   
    class Meta:
        db_table = 'fund_words_lib'