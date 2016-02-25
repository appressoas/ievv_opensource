import elasticsearch_dsl

from ievv_opensource import ievv_elasticsearch2


class CompanyIndexUpdater(ievv_elasticsearch2.IndexUpdater):
    def reindex(self, company, **kwargs):
        company_doctype = self.doctype_class(
            id=company.id,
            name=company.name,
            employee_count=company.employee_set.count()
        )
        return company_doctype.save()

    def reindex_employee_count(self, company, **kwargs):
        self.reindex(company)


class CompanyDocType(ievv_elasticsearch2.DocType):
    indexupdater = CompanyIndexUpdater()

    name = elasticsearch_dsl.String()
    employee_count = elasticsearch_dsl.Integer()

    @classmethod
    def reindex(cls, company):
        pass

    class Meta:
        index = 'main'


class EmployeeIndexUpdater(ievv_elasticsearch2.IndexUpdater):

    def reindex(self, employee, **kwargs):
        employee_doctype = self.doctype_class(
            id=employee.id,
            name=employee.name,
            description=employee.description,
            company_name=employee.company.name
        )
        return employee_doctype.save()

    def reindex_company_name(self, company, **kwargs):
        for employee in company.employee_set.all():
            self.reindex(employee)


class EmployeeDocType(ievv_elasticsearch2.DocType):
    indexupdater = EmployeeIndexUpdater()

    name = elasticsearch_dsl.String()
    description = elasticsearch_dsl.String()
    company_name = elasticsearch_dsl.String()

    class Meta:
        index = 'main'
