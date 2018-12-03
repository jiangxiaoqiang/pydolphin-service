from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import FileField

class Logger(models.Model):
    name = models.CharField(blank=False)

    class Meta:
        db_table = 'logger'