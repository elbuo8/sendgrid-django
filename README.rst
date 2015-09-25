SendGrid-django
===============

Simple django backend to send email using SendGrid's Web API.

Installation
------------

Install the backend from PyPI:

.. code:: bash

    pip install sendgrid-django

Add the following to your project's **settings.py**:

.. code:: python

    EMAIL_BACKEND = "sgbackend.SendGridBackend"
    SENDGRID_API_KEY = "Your SendGrid API Key"

Or, SendGrid username and password can be used instead of an API key:

.. code:: python

    EMAIL_BACKEND = "sgbackend.SendGridBackend"
    SENDGRID_USER = "Your SendGrid Username"
    SENDGRID_PASSWORD = "Your SendGrid Password"

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
    mail.attach_alternative("<p>This is a simple HTML email body</p>", "text/html")

    mail.send()

MIT
---

Enjoy :)
