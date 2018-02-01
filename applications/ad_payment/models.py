from applications.advertisements.models import Advertisement
from django.db import models
from django.utils.translation import gettext as _


class AdvertisementPayment(models.Model):
    """
    to store payments.
    """
    advertisement = models.ForeignKey(Advertisement, related_name="pay_advertisement")
    transaction_id = models.CharField(max_length=234, blank=True)

    class Meta:
        verbose_name = _("Advertisement Payment")
        verbose_name_plural = _("Advertisement Payment")

    def __str__(self):
        return self.transaction_id
