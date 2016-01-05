from django import test
from django.core.exceptions import ValidationError
from model_mommy import mommy

from ievv_opensource.ievv_bulkoperation.models import BulkOperation


class TestBulkOperationModel(test.TestCase):
    def test_clean_status_finished_result_not_available(self):
        bulkoperation = mommy.prepare('ievv_bulkoperation.BulkOperation',
                                      status=BulkOperation.STATUS_FINISHED,
                                      result=BulkOperation.RESULT_NOT_AVAILABLE)
        with self.assertRaisesMessage(ValidationError,
                                      'Must be "successful" or "failed" when status is "finished".'):
            bulkoperation.clean()
