from django.apps import AppConfig

from ievv_opensource import ievv_batchframework
from ievv_opensource import ievv_elasticsearch2
from ievv_opensource.demo.elasticsearch2demo.doctypes import CompanyDocType, EmployeeDocType
from ievv_opensource.ievv_batchframework import batchregistry


class CompanyUpdateFromEmployeesAction(ievv_batchframework.Action):
    def execute(self):
        employee_ids = self.kwargs['ids']
        self.logger.info('Updating index for companies containing the following employees: %r',
                         employee_ids)
        CompanyDocType.indexupdater.bulk_index_by_employee_ids(employee_ids=employee_ids)


class ElasticSearch2DemoAppConfig(AppConfig):
    name = 'ievv_opensource.demo.elasticsearch2demo'
    verbose_name = "IEVV ElasticSearch2 demo"

    def ready(self):
        from ievv_opensource.demo.elasticsearch2demo.doctypes import CompanyDocType
        batchregistry.Registry.get_instance().add_actiongroup(
            batchregistry.ActionGroup(
                name='elasticsearch2demo_company_update',
                actions=[
                    ievv_elasticsearch2.indexaction_factory(doctype_class=CompanyDocType)
                ]))
        batchregistry.Registry.get_instance().add_actiongroup(
            batchregistry.ActionGroup(
                name='elasticsearch2demo_employee_update',
                actions=[
                    ievv_elasticsearch2.indexaction_factory(doctype_class=EmployeeDocType),
                    CompanyUpdateFromEmployeesAction
                ]))
