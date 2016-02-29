from __future__ import absolute_import

import celery


class BatchActionGroupTask(celery.Task):
    abstract = True

    def syncronously_run_actiongroup(self, actiongroup_name, **kwargs):
        # batchoperation.get(....)
        # batchoperation.mark_as_running(....)
        from ievv_opensource.ievv_batchframework import batchregistry
        registry = batchregistry.Registry.get_instance()
        registry.get_actiongroup(actiongroup_name).run_syncronous(kwargs=kwargs,
                                                                  executed_by_celery=True)
        # batchoperation.mark_as_finished(success=True|False)


@celery.shared_task(base=BatchActionGroupTask)
def default(actiongroup_name, **kwargs):
    default.syncronously_run_actiongroup(actiongroup_name=actiongroup_name,
                                         **kwargs)


@celery.shared_task(base=BatchActionGroupTask)
def highpriority(actiongroup_name, **kwargs):
    highpriority.syncronously_run_actiongroup(actiongroup_name=actiongroup_name,
                                              **kwargs)
