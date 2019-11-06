from django import test
from ievv_opensource.ievv_logging.models import IevvLoggingEventBase, IevvLoggingEventItem
from ievv_opensource.ievv_logging.utils import IevvLogging


class TestIevvLogging(test.TestCase):

    def test_begin(self):
        ievvlogging = IevvLogging('foo_bar')
        ievvlogging.begin()
        self.assertEqual(1, IevvLoggingEventBase.objects.count())
        self.assertEqual(1, IevvLoggingEventItem.objects.count())

    def test_finish(self):
        ievvlogging = IevvLogging('foo_bar')
        ievvlogging.begin()
        self.assertEqual(1, IevvLoggingEventBase.objects.count())
        self.assertEqual(1, IevvLoggingEventItem.objects.count())
        ievvlogging.finish()
        self.assertEqual(1, IevvLoggingEventBase.objects.count())
        self.assertEqual(1, IevvLoggingEventItem.objects.count())

    def test_that_no_duplicates_of_slug_is_created(self):
        ievvlogging = IevvLogging('foo_bar')
        ievvlogging.begin()
        ievvlogging2 = IevvLogging('foo_bar')
        ievvlogging2.begin()
        self.assertEqual(1, IevvLoggingEventBase.objects.count())

    def test_each_logging_gives_another_row_in_item_model(self):
        ievvlogging = IevvLogging('foo_bar')
        ievvlogging.begin()
        ievvlogging.finish()
        ievvlogging2 = IevvLogging('foo_bar')
        ievvlogging2.begin()
        ievvlogging2.finish()
        self.assertEqual(1, IevvLoggingEventBase.objects.count())
        self.assertEqual(2, IevvLoggingEventItem.objects.count())

    def test_jsondata_populating(self):
        ievvlogging = IevvLogging('foo_bar')
        ievvlogging.begin()
        a_dictionary = {'a': 'b'}
        ievvlogging.finish(
            foo=1,
            bar=2,
            **a_dictionary
        )
        self.assertTrue('a' in IevvLoggingEventItem.objects.first().data)
        self.assertEqual(3, len(IevvLoggingEventItem.objects.first().data))


