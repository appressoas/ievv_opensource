from django.dispatch import Signal


company_created = Signal(providing_args=["company"])
company_updated = Signal(providing_args=["company"])
employee_created = Signal(providing_args=["employee"])
employee_updated = Signal(providing_args=["employee"])
employee_deleted = Signal(providing_args=["employee"])


def on_company_updated(company, **kwargs):
    pass
    # from ievv_opensource.demo.elasticsearch2demo import celery_tasks
    # celery_tasks.default.delay(company_id=company.id)
