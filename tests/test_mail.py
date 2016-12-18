from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage
from django.test import SimpleTestCase as TestCase

from sgbackend import SendGridBackend

settings.configure()


class SendGridBackendTests(TestCase):
    def test_raises_if_sendgrid_api_key_doesnt_exists(self):
        with self.assertRaises(ImproperlyConfigured):
            SendGridBackend()

    def test_if_not_emails(self):
        with self.settings(SENDGRID_API_KEY='test_key'):
            SendGridBackend().send_messages(emails=[])

    def test_build_empty_sg_mail(self):
        test_email = EmailMessage()
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(test_email)
            self.assertEqual(
                mail,
                {'from': {'email': 'webmaster@localhost'},
                 'subject': '',
                 'content': [{'type': 'text/plain', 'value': ''}],
                 'personalizations': [{'subject': ''}]}
            )
