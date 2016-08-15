from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ievv_opensource.demo.project.settingsproxy')
app = Celery(main='ievv_opensource')
app.config_from_object('django.conf:settings')


# This debug task is only here to make it easier to verify that
# celery is working properly.
@app.task(bind=True)
def debug_add_task(self, a, b):
    print('Request: {!r} - Running {} + {}, and returning the result.'.format(
        self.request, a, b))
    return a + b
