SendGrid-django
===============

.. image:: https://travis-ci.org/elbuo8/sendgrid-django.svg?branch=master
   :target: https://travis-ci.org/elbuo8/sendgrid-django
   :alt: Travis CI
.. image:: https://codecov.io/github/elbuo8/sendgrid-django/coverage.svg?branch=master
   :target: https://codecov.io/github/elbuo8/sendgrid-django
   :alt: codecov.io

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

    # Add categories
    mail.categories = [
        'work',
        'urgent',
    ]

    mail.attach_alternative(
        "<p>This is a simple HTML email body</p>", "text/html"
    )

    mail.send()

To create an instance of a SendGridBackend with an API key other than that provided in settings, pass `api_key` to the constructor

.. code::python

    from sgbackend import SendGridBackend
    from django.core.mail import send_mail

    connection = SendGridBackend(api_key='your key')

    send_mail(<subject etc>, connection=connection)


License
-------
MIT


Enjoy :)


Development
-----------

Install dependencies::
    `pip install -r requirements-dev.txt`

Run the tests with coverage::
    `pytest --cov=sgbackend`

If you see the error "No module named sgbackend", run::
    `pip install -e .`