from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from applications.utils import base_models
from django.db import models


class Category(models.Model):
    """
    Model to store categories.
    """
    category = models.CharField(_('Category'), max_length=50)
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(_('Image'), null=True, blank=True)
    slug = AutoSlugField(populate_from='category', unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.category


class Advertisement(base_models.TimeStampedModelBase):
    """
    Model to store advertisements..
    """
    title = models.CharField(verbose_name=_('Title'), max_length=200)
    description = models.TextField(verbose_name='Description')
    category = models.ForeignKey(Category,related_name="category_advertisement")
    image = models.ImageField(verbose_name=_('Image'), blank=True, null=True)
    address = models.TextField(verbose_name=_('Address'), null=True, blank=True)
    contact_email = models.EmailField(verbose_name=_('Contact Email'))
    contact_number = models.CharField(verbose_name=_('Contact Number'),max_length=30,null=True, blank=True)
    is_featured = models.BooleanField(verbose_name=_('Featured'), default=False)
    created_by = models.ForeignKey(User,related_name="user_advertisement",null=True,blank=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    class Meta:
        verbose_name = _("Advertisement")
        verbose_name_plural = _("Advertisements")

    def __str__(self):
        return str(self.title[:30])
