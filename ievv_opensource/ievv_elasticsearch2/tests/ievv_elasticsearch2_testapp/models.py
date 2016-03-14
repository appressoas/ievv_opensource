import datetime

from django.db import models
from django.utils import timezone


class ModelMapperForeignKeyModel(models.Model):
    name = models.CharField(max_length=255, default='', blank=True)


class ModelmapperModel(models.Model):
    char = models.CharField(max_length=255, default='', blank=True)
    text = models.TextField(default='', blank=True)
    smallint = models.SmallIntegerField(default=0)
    int = models.IntegerField(default=0)
    bigint = models.BigIntegerField(default=0)
    float = models.FloatField(default=0)
    boolean = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today)
    datetime = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(ModelMapperForeignKeyModel)


class ModelMapperChildModel(models.Model):
    modelmappermodel = models.ForeignKey(ModelmapperModel, related_name='children')
    size = models.IntegerField(default=0, blank=True)
