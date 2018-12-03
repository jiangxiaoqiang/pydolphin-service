from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import FileField

class Book(models.Model):
    name = models.CharField(blank=False,max_length=256)
    isbn = models.CharField(blank=False,max_length=16)
    publisher = ArrayField(models.CharField(blank=False,max_length=256))
    author = ArrayField(models.CharField(max_length=256))
    publish_year = models.CharField(max_length=32)
    binding = models.CharField(max_length=128)
    price = models.CharField(max_length=12)
    subtitle = models.CharField(max_length=256)
    original_name = models.CharField(max_length=256)
    translator = ArrayField(models.CharField(max_length=256))
    pages = models.CharField(max_length=32)
    issuer = models.CharField(max_length=8000)
    creator = models.CharField(max_length=128)

    class Meta:
        db_table = 'book'