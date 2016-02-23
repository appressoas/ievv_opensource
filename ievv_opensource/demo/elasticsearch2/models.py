from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal, receiver


class Company(models.Model):
    name = models.CharField(max_length=255)


class Employee(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)
    description = models.TextField()


company_created = Signal(providing_args=["company"])
company_updated = Signal(providing_args=["company"])
employee_created = Signal(providing_args=["employee"])
employee_updated = Signal(providing_args=["employee"])
employee_deleted = Signal(providing_args=["employee"])


@receiver(post_save, sender=Company)
def on_company_post_save(sender, instance, created, **kwargs):
    if created:
        company_created.send(sender=sender, company=instance)
    else:
        company_updated.send(sender=sender, company=instance)


@receiver(post_save, sender=Employee)
def on_employee_post_save(sender, instance, created, **kwargs):
    if created:
        employee_created.send(sender=sender, employee=instance)
    else:
        employee_updated.send(sender=sender, employee=instance)


@receiver(post_delete, sender=Employee)
def on_employee_post_delete(sender, instance, **kwargs):
    employee_deleted.send(sender=sender, employee=instance)
