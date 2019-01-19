from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import FileField

class BookIndustryIdentifiers(models.Model):
    book_id = models.CharField(blank=False,max_length=256)
    type = models.CharField(blank=False,max_length=16)
    identifier = models.CharField(blank=False,max_length=16)

    class Meta:
        db_table = 'book_industry_identifiers'