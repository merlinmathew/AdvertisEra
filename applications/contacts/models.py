from django.utils.translation import gettext as _
from applications.utils import base_models
from django.db import models
from solo.models import SingletonModel


class Contact(base_models.TimeStampedModelBase):
    """
    Model to store contacts.
    """
    name = models.CharField(_('Name'), max_length=50)
    email = models.EmailField(_('Email'))
    message = models.TextField(verbose_name='Message')

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return self.name


class AdvertiseraAddress(SingletonModel):
    """
     To Store the Bank Address
    """
    company = models.CharField(verbose_name=_('Company'), max_length=50)
    phone = models.CharField(verbose_name=_('Phone'), max_length=50)
    email = models.EmailField(verbose_name=_('Email'))
    address = models.TextField(verbose_name=_('Address'))

    class Meta:
        verbose_name = _("Advertisera Address")

    def __str__(self):
        return self.company
