from django.apps import AppConfig

from ievv_opensource.ievv_batchframework import batchregistry


class ElasticSearch2DemoAppConfig(AppConfig):
    name = 'ievv_opensource.demo.elasticsearch2demo'
    verbose_name = "IEVV ElasticSearch2 demo"

    def ready(self):
        batchregistry.Registry.get_instance().add_actiongroup(
            batchregistry.ActionGroup(
                name='elasticsearch2demo_company_update',
                # mode=ActionGroup.MODE_SYNCHRONOUS,
                # route_to_alias=batchregistry.Registry.ROUTE_TO_ALIAS_HIGHPRIORITY,
                actions=[
                    batchregistry.Action
                ]))
