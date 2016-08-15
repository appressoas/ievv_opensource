from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from ievv_opensource.ievv_batchframework import batchregistry


class Company(models.Model):
    name = models.CharField(max_length=255)


class Employee(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)
    description = models.TextField()
