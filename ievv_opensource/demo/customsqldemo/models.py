# -*- coding: utf-8 -*-
from django.db import models


class Person(models.Model):
    name = models.CharField(
        max_length=255)
    description = models.TextField(
        null=False, blank=True, default='')

    def __str__(self):
        return self.name
