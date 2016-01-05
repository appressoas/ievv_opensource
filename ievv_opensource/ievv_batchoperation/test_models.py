from django import test
from django.core.exceptions import ValidationError
from model_mommy import mommy

from ievv_opensource.ievv_batchoperation.models import BatchOperation


class TestBulkOperationModel(test.TestCase):
    def test_clean_status_finished_result_not_available(self):
        bulkoperation = mommy.prepare('ievv_batchoperation.BatchOperation',
                                      status=BatchOperation.STATUS_FINISHED,
                                      result=BatchOperation.RESULT_NOT_AVAILABLE)
        with self.assertRaisesMessage(ValidationError,
                                      'Must be "successful" or "failed" when status is "finished".'):
            bulkoperation.clean()

    def test_input_data_setter(self):
        bulkoperation = mommy.prepare('ievv_batchoperation.BatchOperation')
        bulkoperation.input_data = {'hello': 'world'}
        self.assertEqual(
            '{"hello": "world"}',
            bulkoperation.input_data_json)

    def test_input_data_getter_emptystring(self):
        bulkoperation = mommy.prepare('ievv_batchoperation.BatchOperation',
                                      input_data_json='')
        self.assertEqual(
            None,
            bulkoperation.input_data)

    def test_input_data_getter_nonemptystring(self):
        bulkoperation = mommy.prepare('ievv_batchoperation.BatchOperation',
                                      input_data_json='{"hello": "world"}')
        self.assertEqual(
            {'hello': 'world'},
            bulkoperation.input_data)

    def test_output_data_setter(self):
        bulkoperation = mommy.prepare('ievv_batchoperation.BatchOperation')
        bulkoperation.output_data = {'hello': 'world'}
        self.assertEqual(
            '{"hello": "world"}',
            bulkoperation.output_data_json)

    def test_output_data_getter_emptystring(self):
        bulkoperation = mommy.prepare('ievv_batchoperation.BatchOperation',
                                      output_data_json='')
        self.assertEqual(
            None,
            bulkoperation.output_data)

    def test_output_data_getter_nonemptystring(self):
        bulkoperation = mommy.prepare('ievv_batchoperation.BatchOperation',
                                      output_data_json='{"hello": "world"}')
        self.assertEqual(
            {'hello': 'world'},
            bulkoperation.output_data)
