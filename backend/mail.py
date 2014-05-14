from django.core.mail.backends.base import BaseEmailBackend
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import sendgrid

class SendGridBackend(BaseEmailBackend):
    '''
    SendGrid Web API Backend
    '''
    def __init__(self, **kwargs):
        super(SendGridBackend).__init__(**kwargs)
        self.api_user = getattr(settings, "SENDGRID_USER", None)
        self.api_key =  getattr(settings, "SENDGRID_PASSWORD", None)

        if self.api_user == None or self.api_key == None:
            raise ImproperlyConfigured('''Either SENDGRID_USER or SENDGRID_PASSWORD
                was not declared in settings.py''')
        self.sg = sendgrid.SendGridClient(self.api_user, self.api_key, raise_errors=True)

    def send_messages(self, emails):
        '''
        Comments
        '''
        if not emails:
            return
        count = 0
        for email in emails:
            status, msg = self.sg.send(email)
            if status == 200:
                count += 1
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
                mail.set_replyto(email.extra_headers["Reply-To"])

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

            for attachment in email.attachment:
                mail.add_attachment_stream(attachment.Name, attachment.Content)

        return mail