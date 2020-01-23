try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

from django.core.mail import EmailMessage
from django.test import SimpleTestCase

from sgbackend import SendGridBackend


class SendMessagesTestCase(SimpleTestCase):
    """Tests for SendGridBackend.test_messages()."""

    def setUp(self):
        self.test_message = EmailMessage(
            subject="Test email message",
            body="Lorem ipsum!",
            from_email="example@example.com",
            to=["example2@example.com"],
        )

    def test_sending_without_emails(self):
        """
        Verify that send_messages returns nothing if no messages are passed.
        """
        sendgrid_backend = SendGridBackend(api_key="test")
        self.assertEqual(sendgrid_backend.send_messages(emails=[]), None)

    def test_sending(self):
        """Verify that send_messages returns sent count if message is sent."""
        sendgrid_backend = SendGridBackend(api_key="test")
        sendgrid_backend.sg.client = Mock()
        self.assertEqual(
            sendgrid_backend.send_messages(emails=[self.test_message]), 1
        )

    def test_failing_silently(self):
        """Verify that send_messages can fail silently."""
        sendgrid_backend = SendGridBackend(api_key="test")
        sendgrid_backend.sg.client = Mock()
        http_error = HTTPError(url="", code=999, msg=None, hdrs=None, fp=None)
        sendgrid_backend.sg.client.mail.send.post = Mock(
            side_effect=http_error
        )

        self.assertFalse(sendgrid_backend.fail_silently)
        with self.assertRaises(HTTPError):
            sendgrid_backend.send_messages(emails=[self.test_message])

        sendgrid_backend.fail_silently = True
        self.assertEqual(
            sendgrid_backend.send_messages(emails=[self.test_message]), 0
        )
