import unittest

from django.core.exceptions import ImproperlyConfigured

from sgbackend import SendGridBackend


class SendGridBackendTests(unittest.TestCase):
    def test_raises_if_sendgrid_api_key_doesnt_exists(self):
        with self.assertRaises(ImproperlyConfigured):
            SendGridBackend()
