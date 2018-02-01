from applications.advertisements.models import Advertisement, Category
from applications.contacts.models import AdvertiseraAddress
from applications.likes.models import Like

from django import template

__author__ = 'Merlin'

register = template.Library()


@register.assignment_tag()
def advertisement_list():
    advertisements = Advertisement.objects.order_by('id')
    return advertisements


@register.assignment_tag()
def category_list():
    categories = Category.objects.all()
    return categories


@register.assignment_tag()
def get_address():
    address = AdvertiseraAddress.objects.get()
    return address


@register.assignment_tag()
def get_like(user,advertisement):
    likes = Like.objects.filter(user=user,advertisement=advertisement).exists()
    return likes
