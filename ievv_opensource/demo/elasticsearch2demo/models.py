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


@receiver(post_save, sender=Company)
def on_company_post_save(sender, instance, created, **kwargs):
    company = instance
    if created:
        pass
    else:
        executioninfo = batchregistry.Registry.get_instance().run(
            actiongroup_name='elasticsearch2demo_company_update',
            context_object=company,
            started_by=get_user_model().objects.first(),
            ids=[instance.id]
        )
        print()
        print("*" * 70)
        print()
        print('executioninfo', executioninfo)
        print()
        print("*" * 70)
        print()
