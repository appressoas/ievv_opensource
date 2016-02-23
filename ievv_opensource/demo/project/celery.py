from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ievv_opensource.demo.project.settingsproxy')

app = Celery('ievv_opensource')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks([
    'ievv_opensource.ievv_elasticsearch2.indexingmanager',
])


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
