from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models

from applications.utils import base_models
from applications.advertisements.models import Advertisement


class Like(base_models.TimeStampedModelBase):
    """
    to store details about a like made by users
    """
    user = models.ForeignKey(User,related_name='user_likes')
    advertisement = models.ForeignKey(Advertisement,related_name='likes')


    class Meta():
        abstract = False
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')

    def __str__(self):
        return str(self.advertisement)


