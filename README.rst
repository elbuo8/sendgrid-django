django-sgapi
============

A Django email backend for the SendGrid API

Installation
------------

Install the backend from PyPI:

.. code:: bash

    pip install django-sgapi

Add the following to your project's **settings.py**:

.. code:: python

    EMAIL_BACKEND = "sgbackend.SendGridBackend"
    SENDGRID_API_KEY = "Your SendGrid API Key"

**Done!**

Example
-------

.. code:: python


    from django.core.mail import send_mail
    from django.core.mail import EmailMultiAlternatives

    send_mail("Your Subject", "This is a simple text email body.",
      "Yamil Asusta <hello@yamilasusta.com>", ["yamil@sendgrid.com"])

    # or
    mail = EmailMultiAlternatives(
      subject="Your Subject",
      body="This is a simple text email body.",
      from_email="Yamil Asusta <hello@yamilasusta.com>",
      to=["yamil@sendgrid.com"],
      headers={"Reply-To": "support@sendgrid.com"}
    )
    # Add template
    mail.template_id = 'YOUR TEMPLATE ID FROM SENDGRID ADMIN'

    # Replace substitutions in sendgrid template
    mail.substitutions = {'%username%': 'elbuo8'}

    # Attach file
    with open('somefilename.pdf', 'rb') as file:
        mail.attachments = [
            ('somefilename.pdf', file.read(), 'application/pdf')
        ]

    mail.attach_alternative(
        "<p>This is a simple HTML email body</p>", "text/html"
    )

    mail.send()


License
-------
MIT


Enjoy :)