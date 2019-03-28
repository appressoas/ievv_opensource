from django.test import TestCase
from cradmin_legacy.datetimeutils import default_timezone_datetime

from ievv_opensource.ievv_elasticsearch import jsondecode


class JsonDecode(TestCase):
    def test_datetime(self):
        self.assertEqual(
            jsondecode.datetime(default_timezone_datetime(2015, 1, 1).isoformat()),
            default_timezone_datetime(2015, 1, 1))
