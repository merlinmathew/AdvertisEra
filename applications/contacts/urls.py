__author__ = 'Merlin'

from .views import ContactView

from django.conf.urls import url

urlpatterns = [
    url(r'^us/$', ContactView.as_view(), name='contact'),
]