from __future__ import absolute_import

from celery import shared_task


@shared_task
def default(actiongroup_name, **kwargs):
    from ievv_opensource.ievv_batchframework import batchregistry
    registry = batchregistry.Registry.get_instance()
    registry.get_actiongroup(actiongroup_name).run_syncronous(**kwargs)
