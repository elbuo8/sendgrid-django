from django.core.mail.backends.base import BaseEmailBackend
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from email.mime.base import MIMEBase
import sendgrid
import base64
from sendgrid.helpers.mail import *

try:
    import rfc822
except Exception as e:
    import email.utils as rfc822


class SendGridBackend(BaseEmailBackend):
    '''
    SendGrid Web API Backend
    '''
    def __init__(self, fail_silently=False, **kwargs):
        super(SendGridBackend, self).__init__(
            fail_silently=fail_silently, **kwargs)
        self.api_key = getattr(settings, "SENDGRID_API_KEY", None)

        if self.api_key:
            self.sg = sendgrid.SendGridAPIClient(
                apikey=self.api_key)
        else:
            raise ImproperlyConfigured('''
                SENDGRID_API_KEY must be declared in settings.py''')

    def open(self):
        pass

    def close(self):
        pass

    def send_messages(self, emails):
        '''
        Comments
        '''
        if not emails:
            return

        count = 0
        for email in emails:
            mail = self._build_sg_mail(email)
            response = self.sg.client.mail.send.post(request_body=mail)
            count += 1

        return count

    def _build_sg_mail(self, email):
        mail = Mail()
        mail.set_from(Email(email.from_email))
        mail.set_subject(email.subject)

        personalization = Personalization()
        for e in email.to:
            personalization.add_to(Email(e))
        for e in email.cc:
            personalization.add_cc(Email(e))
        for e in email.bcc:
            personalization.add_bcc(Email(e))
        personalization.set_subject(email.subject)
        mail.add_content(Content("text/plain", email.body))
        if isinstance(email, EmailMultiAlternatives):
            for alt in email.alternatives:
                if alt[1] == "text/html":
                    mail.add_content(Content(alt[1], alt[0]))
        elif email.content_subtype == "html":
            mail.contents = []
            mail.add_content(Content("text/plain", ' '))
            mail.add_content(Content("text/html", email.body))

        for attachment in email.attachments:
            if isinstance(attachment, MIMEBase):
                attach = Attachment()
                attach.set_filename(attachment.get_filename())
                attach.set_content(base64.b64encode(attachment.get_payload()))
                mail.add_attachment(attach)
            elif isinstance(attachment, tuple):
                attach = Attachment()
                attach.set_filename(attachment[0])
                attach.set_content(base64.b64encode(attachment[1]))
                attach.set_type(attachment[2])
                mail.add_attachment(attach)

                # if email.extra_headers:
                # if "Reply-To" in email.extra_headers:
                # reply_to = rfc822.parseaddr(email.extra_headers["Reply-To"])[1]
                # personalization.set_replyto(reply_to)

                # if "Subs" in email.extra_headers:
                #    mail.set_substitutions(email.extra_headers["Subs"])

                # if "Sections" in email.extra_headers:
                #    mail.set_sections(email.extra_headers["Sections"])

                # if "Categories" in email.extra_headers:
                #    mail.set_categories(email.extra_headers["Categories"])

                # if "Unique-Args" in email.extra_headers:
                #    mail.set_unique_args(email.extra_headers["Unique-Args"])

                # if "Filters" in email.extra_headers:
                #    mail.smtpapi.data['filters'] = email.extra_headers["Filters"]

                # for attachment in email.attachments:
                #    mail.add_attachment_stream(attachment[0], attachment[1])

        mail.add_personalization(personalization)
        return mail.get()
