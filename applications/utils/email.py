__author__ = 'Merlin'
import re
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def valid_email(email):
    return re.match("[^@]+@[^@]+\.[^@]+", email)


def advertisera_mail(to, subject, body, link=None, bcc=None, attachments=None, attachment_name=None,
             template=None, from_email=None):
    if bcc:
        bcc = [bcc]

    if not template:
        template = 'common/email.html'

    # if not attachment_name:
    #     attachment_name = 'Attachment.pdf'

    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    html = render_to_string(
        template,
        {
            'title': subject,
            'content': body,
            'link': link,
        }
    )

    plain = strip_tags(html)

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain,
        from_email=from_email,
        to=[to],
        bcc=bcc
    )

    email.attach_alternative(html, 'text/html')

    email.attach(attachment_name, attachments, "application/pdf") if attachments else None

    email.send()
