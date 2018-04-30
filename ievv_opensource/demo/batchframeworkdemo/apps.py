from django.apps import AppConfig

from ievv_opensource import ievv_batchframework
from ievv_opensource.ievv_batchframework import batchregistry


class HelloWorldAction(ievv_batchframework.Action):
    def execute(self):
        self.logger.info('Hello world! %r', self.kwargs)


class HelloWorldAsyncAction(ievv_batchframework.Action):
    def execute(self):
        self.logger.info('\n\n\n\n\n\n\n\nHello world, async! %r\n\n\n\n\n', self.kwargs)


class BatchFrameworkDemoAppConfig(AppConfig):
    name = 'ievv_opensource.demo.batchframeworkdemo'
    verbose_name = "IEVV Batchframework demo"

    def ready(self):
        batchregistry.Registry.get_instance().add_actiongroup(
            batchregistry.ActionGroup(
                name='batchframeworkdemo_helloworld',
                mode=batchregistry.ActionGroup.MODE_SYNCHRONOUS,
                actions=[
                    HelloWorldAction
                ]))
        batchregistry.Registry.get_instance().add_actiongroup(
            batchregistry.ActionGroup(
                name='batchframeworkdemo_helloworld_async',
                mode=batchregistry.ActionGroup.MODE_ASYNCHRONOUS,
                actions=[
                    HelloWorldAsyncAction
                ]
            )
        )
