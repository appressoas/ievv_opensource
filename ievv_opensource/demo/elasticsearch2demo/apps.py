from django.apps import AppConfig

from ievv_opensource import ievv_elasticsearch2
from ievv_opensource.ievv_batchframework import batchregistry


class ElasticSearch2DemoAppConfig(AppConfig):
    name = 'ievv_opensource.demo.elasticsearch2demo'
    verbose_name = "IEVV ElasticSearch2 demo"

    def ready(self):
        from ievv_opensource.demo.elasticsearch2demo.doctypes import CompanyDocType
        # batchregistry.Registry.get_instance().add_actiongroup(
        #     batchregistry.ActionGroup(
        #         name='elasticsearch2demo_company_update',
                # mode=batchregistry.ActionGroup.MODE_SYNCHRONOUS,
                # route_to_alias=batchregistry.Registry.ROUTE_TO_ALIAS_HIGHPRIORITY,
        #        actions=[
        #             batchregistry.Action
        #         ]))
        batchregistry.Registry.get_instance().add_actiongroup(
            batchregistry.ActionGroup(
                name='elasticsearch2demo_company_update',
                # mode=batchregistry.ActionGroup.MODE_SYNCHRONOUS,
                # route_to_alias=batchregistry.Registry.ROUTE_TO_ALIAS_HIGHPRIORITY,
                actions=[
                    ievv_elasticsearch2.indexaction_factory(doctype_class=CompanyDocType)
                ]))
