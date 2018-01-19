from .views import HomeView, RegisterView, LoginView, AddAdvertisementView, AdvertisementDetailView, \
    AdvertisementEditView, AboutView, CategoryListingView, AccountActivationView
from . import views
__author__ = 'Merlin'


from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^add-advertisement/$', AddAdvertisementView.as_view(), name='add-advertisement'),
    url(r'^advertisement-detail/(?P<slug>[-\w]+)/$', AdvertisementDetailView.as_view(), name='advertisement-detail'),
    url(r'^advertisement-edit/(?P<slug>[-\w]+)/$', AdvertisementEditView.as_view(), name='advertisement-edit'),
    url(r'^category-listing/(?P<slug>[-\w]+)/$', CategoryListingView.as_view(), name='category-listing'),
    url(r'^contact/$', HomeView.as_view(), name='contact'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        AccountActivationView.as_view(), name='activate'),
    url(r'^charge/$', views.charge, name="charge"),
]