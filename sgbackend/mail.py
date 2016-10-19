import base64
import sys
import urllib
from email.mime.base import MIMEBase

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.base import BaseEmailBackend

import sendgrid
from sendgrid.helpers.mail import (
    Attachment,
    Category,
    Content,
    Email,
    Mail,
    Personalization,
    Substitution
)


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
            try:
                self.sg.client.mail.send.post(request_body=mail)
                count += 1
            except urllib.error.HTTPError as e:
                if not self.fail_silently:
                    raise
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

        if hasattr(email, 'categories'):
            for c in email.categories:
                mail.add_category(Category(c))

        if hasattr(email, 'template_id'):
            mail.set_template_id(email.template_id)
            if hasattr(email, 'substitutions'):
                for k, v in email.substitutions.items():
                    personalization.add_substitution(Substitution(k, v))

        for attachment in email.attachments:
            if isinstance(attachment, MIMEBase):
                attach = Attachment()
                attach.set_filename(attachment.get_filename())
                attach.set_content(base64.b64encode(attachment.get_payload()))
                mail.add_attachment(attach)
            elif isinstance(attachment, tuple):
                attach = Attachment()
                attach.set_filename(attachment[0])
                base64_attachment = base64.b64encode(attachment[1])
                if sys.version_info >= (3,):
                    attach.set_content(str(base64_attachment, 'utf-8'))
                else:
                    attach.set_content(base64_attachment)
                attach.set_type(attachment[2])
                mail.add_attachment(attach)

        mail.add_personalization(personalization)
        return mail.get()
