from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import FileField

class ApiResponse(models.Model):    
    code = models.CharField(blank=True,max_length=256)
    message = ArrayField(models.CharField(max_length=256))
    data = models.CharField(blank=True,max_length=32)