from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ievv_opensource.demo.elasticsearch2demo import elasticsearch2demo_signals
from ievv_opensource.ievv_batchframework import batchregistry


class Company(models.Model):
    name = models.CharField(max_length=255)


class Employee(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)
    description = models.TextField()


@receiver(post_save, sender=Company)
def on_company_post_save(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        batchregistry.Registry.get_instance().run(
            actiongroup_name='elasticsearch2demo_company_update',
            company_id=instance.id)


# @receiver(post_save, sender=Employee)
# def on_employee_post_save(sender, instance, created, **kwargs):
#     if created:
#         elasticsearch2demo_signals.employee_created.send(sender=sender, employee=instance)
#     else:
#         # elasticsearch2demo_signals.employee_updated.send(sender=sender, employee=instance)
#         batchregistry.Registry.get_instance().run('elasticsearch2demo_company_update', company=instance)


# @receiver(post_delete, sender=Employee)
# def on_employee_post_delete(sender, instance, **kwargs):
#     elasticsearch2demo_signals.employee_deleted.send(sender=sender, employee=instance)
#     # registry = ievv_elasticsearch2.indexingmanager.Registry.get_instance()
#     # result = registry.index('devilry_assignments_namechange',
#     #                         assignments=[instance])
#     # if result.has_background_tasks():
#     # else:
