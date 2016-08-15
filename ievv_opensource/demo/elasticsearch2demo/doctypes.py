from ievv_opensource import ievv_elasticsearch2
from ievv_opensource.demo.elasticsearch2demo.models import Company, Employee


class CompanyIndexUpdater(ievv_elasticsearch2.IndexUpdater):
    def bulk_index_by_employee_ids(self, employee_ids):
        company_ids = Company.objects.filter(employee__id__in=employee_ids)\
            .distinct()\
            .values_list('id')
        self.bulk_index_model_ids(ids=company_ids)

    def make_queryset_from_model_ids(self, ids):
        queryset = super(CompanyIndexUpdater, self).make_queryset_from_model_ids(ids=ids)
        return queryset.prefetch_related('employee_set')


class CompanyDocType(ievv_elasticsearch2.ModelDocType):
    model_class = Company
    indexupdater = CompanyIndexUpdater()

    class Meta:
        index = 'main'


class EmployeeDocType(ievv_elasticsearch2.ModelDocType):
    model_class = Employee

    class Meta:
        index = 'main'
