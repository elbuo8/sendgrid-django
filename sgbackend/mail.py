from django.core.mail.backends.base import BaseEmailBackend
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from email.mime.base import MIMEBase
import sendgrid

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
        self.api_user = getattr(settings, "SENDGRID_USER", None)
        self.api_password = getattr(settings, "SENDGRID_PASSWORD", None)

        credentials = []
        if self.api_key:
            credentials.append(self.api_key)
        elif self.api_user and self.api_password:
            credentials.append(self.api_user)
            credentials.append(self.api_password)
        else:
            raise ImproperlyConfigured('''
                Either SENDGRID_API_KEY or both (SENDGRID_USER and
                SENDGRID_PASSWORD) must be declared in settings.py''')
        self.sg = sendgrid.SendGridClient(
            *credentials,
            raise_errors=not fail_silently)

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
            try:
                self.sg.send(self._build_sg_mail(email))
                count += 1
            except sendgrid.SendGridClientError:
                if not self.fail_silently:
                    raise
            except sendgrid.SendGridServerError:
                if not self.fail_silently:
                    raise

        return count

    def _build_sg_mail(self, email):
        mail = sendgrid.Mail()
        mail.add_to(email.to)
        mail.add_cc(email.cc)
        mail.add_bcc(email.bcc)
        mail.set_text(email.body)
        mail.set_subject(email.subject)
        mail.set_from(email.from_email)

        if isinstance(email, EmailMultiAlternatives):
            for alt in email.alternatives:
                if alt[1] == "text/html":
                    mail.set_html(alt[0])

        for attachment in email.attachments:
            if isinstance(attachment, MIMEBase):
                mail.add_attachment_stream(
                    attachment.get_filename(),
                    attachment.get_payload())
            elif isinstance(attachment, tuple):
                mail.add_attachment_stream(attachment[0], attachment[1])

        if email.extra_headers:
            if "Reply-To" in email.extra_headers:
                reply_to = rfc822.parseaddr(email.extra_headers["Reply-To"])[1]
                mail.set_replyto(reply_to)

            if "Subs" in email.extra_headers:
                mail.set_substitutions(email.extra_headers["Subs"])

            if "Sections" in email.extra_headers:
                mail.set_sections(email.extra_headers["Sections"])

            if "Categories" in email.extra_headers:
                mail.set_categories(email.extra_headers["Categories"])

            if "Unique-Args" in email.extra_headers:
                mail.set_unique_args(email.extra_headers["Unique-Args"])

            if "Filters" in email.extra_headers:
                mail.smtpapi.data['filters'] = email.extra_headers["Filters"]

            for attachment in email.attachments:
                mail.add_attachment_stream(attachment[0], attachment[1])

        return mail
