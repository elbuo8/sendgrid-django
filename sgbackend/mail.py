from django.core.mail.backends.base import BaseEmailBackend
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
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
        super(SendGridBackend, self).__init__(fail_silently=fail_silently, **kwargs)
        self.api_user = getattr(settings, "SENDGRID_USER", None)
        self.api_key =  getattr(settings, "SENDGRID_PASSWORD", None)

        if self.api_user == None or self.api_key == None:
            raise ImproperlyConfigured('''Either SENDGRID_USER or SENDGRID_PASSWORD
                was not declared in settings.py''')
        self.sg = sendgrid.SendGridClient(self.api_user, self.api_key, raise_errors= not fail_silently)

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
        mail.set_text(email.body)
        mail.set_subject(email.subject)
        mail.set_from(email.from_email)

        if isinstance(email, EmailMultiAlternatives):
            for alt in email.alternatives:
                if alt[1] == "text/html":
                    mail.set_html(alt[0])

        if email.extra_headers:
            if "Reply-To" in email.extra_headers:
                reply_to = rfc822.parseaddr(email.extra_headers["Reply-To"])[1]
                mail.set_replyto(reply_to)

            if "Subs" in email.extra_headers:
                mail.set_substitutions(email.extra_headers["Sub"])

            if "Sections" in email.extra_headers:
                mail.set_sections(email.extra_headers["Section"])

            if "Categories" in email.extra_headers:
                mail.set_categories(email.extra_headers["Category"])

            if "Unique-Args" in email.extra_headers:
                mail.set_unique_args(email.extra_headers["Unique-Args"])

            if "Filters" in email.extra_headers:
                mail.data['filters'] = email.extra_headers["Filters"]

            for attachment in email.attachments:
                mail.add_attachment_stream(attachment.Name, attachment.Content)

        return mail
