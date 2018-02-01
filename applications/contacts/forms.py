from applications.utils.email import advertisera_mail
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse

__author__ = 'Merlin'
from django.contrib.auth.models import User
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    form for contact purpose.
    """
    class Meta:
        model = Contact
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name*'
        self.fields['email'].widget.attrs['placeholder'] = 'Email*'
        self.fields['message'].widget.attrs['placeholder'] = 'Message*'

    # def save(self, commit=True):
    #     name = self.cleaned_data['name']
    #     email = self.cleaned_data['email']
    #     message = self.cleaned_data['message']
    #
    #     instance = super(ContactForm, self).save(commit=True)
    #
    #     info_body = (
    #         'A new enquiry has been received. '
    #         'View the feedback here: {0}{1}<br/><br/>'
    #         'Name: {2}<br/>Email: {3}<br/>Message: {4}'
    #     ).format(
    #         Site.objects.get_current(),
    #         reverse('contact:contact_response', args=[instance.id]),
    #         name,
    #         email,
    #         message
    #     )
    #
    #     advertisera_mail(
    #         settings.ADMIN_EMAIL,
    #         "[ORA Dev] New Enquiry Received",
    #         info_body
    #     )
    #
    #     return True



