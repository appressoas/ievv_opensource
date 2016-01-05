from unittest import mock

from django import test
from django.core.exceptions import ValidationError
from django_cradmin import datetimeutils
from model_mommy import mommy

from ievv_opensource.ievv_batchoperation.models import BatchOperation


class TestBatchOperationModel(test.TestCase):
    def test_clean_status_finished_result_not_available(self):
        batchoperation = mommy.prepare('ievv_batchoperation.BatchOperation',
                                       status=BatchOperation.STATUS_FINISHED,
                                       result=BatchOperation.RESULT_NOT_AVAILABLE)
        with self.assertRaisesMessage(ValidationError,
                                      'Must be "successful" or "failed" when status is "finished".'):
            batchoperation.clean()

    def test_input_data_setter(self):
        batchoperation = mommy.prepare('ievv_batchoperation.BatchOperation')
        batchoperation.input_data = {'hello': 'world'}
        self.assertEqual(
            '{"hello": "world"}',
            batchoperation.input_data_json)

    def test_input_data_getter_emptystring(self):
        batchoperation = mommy.prepare('ievv_batchoperation.BatchOperation',
                                       input_data_json='')
        self.assertEqual(
            None,
            batchoperation.input_data)

    def test_input_data_getter_nonemptystring(self):
        batchoperation = mommy.prepare('ievv_batchoperation.BatchOperation',
                                       input_data_json='{"hello": "world"}')
        self.assertEqual(
            {'hello': 'world'},
            batchoperation.input_data)

    def test_output_data_setter(self):
        batchoperation = mommy.prepare('ievv_batchoperation.BatchOperation')
        batchoperation.output_data = {'hello': 'world'}
        self.assertEqual(
            '{"hello": "world"}',
            batchoperation.output_data_json)

    def test_output_data_getter_emptystring(self):
        batchoperation = mommy.prepare('ievv_batchoperation.BatchOperation',
                                       output_data_json='')
        self.assertEqual(
            None,
            batchoperation.output_data)

    def test_output_data_getter_nonemptystring(self):
        batchoperation = mommy.prepare('ievv_batchoperation.BatchOperation',
                                       output_data_json='{"hello": "world"}')
        self.assertEqual(
            {'hello': 'world'},
            batchoperation.output_data)

    def test_finish_successful(self):
        batchoperation = mommy.prepare('ievv_batchoperation.BatchOperation')
        batchoperation.finish()
        self.assertEqual(BatchOperation.RESULT_SUCCESSFUL, batchoperation.result)

    def test_finish_failed(self):
        batchoperation = mommy.prepare('ievv_batchoperation.BatchOperation')
        mocknow = datetimeutils.default_timezone_datetime(2016, 1, 1)
        with mock.patch('ievv_opensource.ievv_batchoperation.models.timezone.now', lambda: mocknow):
            batchoperation.finish(failed=True)
        self.assertEqual(BatchOperation.RESULT_FAILED, batchoperation.result)
        self.assertEqual('', batchoperation.output_data_json)
        self.assertEqual(batchoperation.finished_datetime, mocknow)

    def test_finish_with_output_data(self):
        batchoperation = mommy.make('ievv_batchoperation.BatchOperation')
        batchoperation.finish(output_data={'hello': 'world'})
        batchoperation = BatchOperation.objects.get(id=batchoperation.id)
        self.assertEqual(
            '{"hello": "world"}',
            batchoperation.output_data_json)


class TestBatchOperationManager(test.TestCase):
    def test_create_syncronous(self):
        batchoperation = BatchOperation.objects.create_syncronous()
        self.assertEqual(BatchOperation.STATUS_RUNNING, batchoperation.status)

    def test_create_syncronous_with_inputdata(self):
        batchoperation = BatchOperation.objects.create_syncronous(
            input_data={'hello': 'world'})
        self.assertEqual(
            '{"hello": "world"}',
            batchoperation.input_data_json)

    def test_create_asyncronous(self):
        batchoperation = BatchOperation.objects.create_asyncronous()
        self.assertEqual(BatchOperation.STATUS_UNPROCESSED, batchoperation.status)

    def test_create_asyncronous_with_inputdata(self):
        batchoperation = BatchOperation.objects.create_asyncronous(
            input_data={'hello': 'world'})
        self.assertEqual(
            '{"hello": "world"}',
            batchoperation.input_data_json)
