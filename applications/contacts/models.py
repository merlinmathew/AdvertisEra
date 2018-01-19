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
        return str(self.name[:10])+"..."

class AdvertiseraAddress(SingletonModel):
    """
     To Store the Bank Address
    """
    company = models.CharField(verbose_name=_('Company'), max_length=50)
    phone = models.CharField(verbose_name=_('Phone'), max_length=50)
    email = models.EmailField(verbose_name=_('Email'))
    address = models.TextField(verbose_name=_('Address'))

    class Meta:
        verbose_name = _("AdvertiseraAddress")

    def __str__(self):
        return self.company

# class SocialIconsSetting(models.Model):
#     """
#     Admin's control over the social media icons.
#     """
#     TAB_CHOICES = (
#         ('_blank', 'Open_in_new_tab'),
#         ('_parent', 'Open_in_current_tab'),
#     )
#     ICON_CHOICES = (
#         ('facebook', 'Facebook'),
#         ('twitter', 'Twitter'),
#         ('Instagram', 'Instagram'),
#     )
#     icon = models.CharField(max_length=10, choices=ICON_CHOICES)
#     url = models.CharField(max_length=60)
#     sort_order = models.IntegerField()
#     target = models.CharField(max_length=10, choices=TAB_CHOICES)
#     publish = models.BooleanField(default=True)
#
#     class Meta:
#         abstract = False
#         verbose_name = _('Social Icons')
#         verbose_name_plural = _('Social Icons Settings')
#
#     def __str__(self):
#         return self.icon

