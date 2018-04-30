from django import test

from ievv_opensource.ievv_developemail.email_backend import DevelopEmailBackend


class TestDevelopEmailBackend(test.TestCase):
    def test_send_messages(self):
        DevelopEmailBackend().send_messages()
