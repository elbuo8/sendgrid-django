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

    mail.attach_alternative(
        "<p>This is a simple HTML email body</p>", "text/html"
    )

    mail.send()

Example of section usage
------------------------

.. code:: python


    mail = EmailMultiAlternatives(
      subject="A Subject",
      body="This is a simple text email body.",
      from_email="Some Person <hello@example.com>",
      to=["another_person@example.com"],
      headers={"Reply-To": "support@sendgrid.com"}
    )
    # Add template
    mail.template_id = 'YOUR TEMPLATE ID FROM SENDGRID ADMIN'

    html_content = "<b>%subst-1%</b> and %subst-2%"
    mail.attach_alternative(html_content, 'text/html', )

    # Section substitutions you specify here will be used when the template is rendered
    # See the 'section' docs @ sendgrid
    mail.substitutions = {
      '%subst-1%': 'Lets put %section-1%',
      '%subst-2%': '%section-2%'
    }
    mail.sections = {
      '%section-1%': 'some interesting content here',
      '%section-2%': '(more interesting content, up to 10k bytes)',
    }

    mail.send()


Section usage result
----------
    **Lets put some interesting content here**. Here is something else: (more interesting content, up to 10k bytes)


License
-------
MIT


Enjoy :)
