__author__ = 'Merlin'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db import fields


class TimeStampedModelBase(models.Model):
    """ TimeStampedModel
    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """
    created = fields.CreationDateTimeField(verbose_name=_('Created'))
    modified = fields.ModificationDateTimeField(verbose_name=_('Modified'))

    class Meta:
        abstract = True