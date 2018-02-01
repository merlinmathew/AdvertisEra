__author__ = 'Merlin'

from .views import HomeView, RegisterView, LoginView, AddAdvertisementView, AdvertisementDetailView, \
    AdvertisementEditView, AboutView, CategoryListingView, AccountActivationView, AdvertisementDeleteView, \
    LikeView, SearchAdView, PayView, InactiveLinkView
from . import views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', HomeView.as_view(),name="home"),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^add-advertisement/$', AddAdvertisementView.as_view(), name='add-advertisement'),
    url(r'^advertisement-detail/(?P<slug>[-\w]+)/$', AdvertisementDetailView.as_view(), name='advertisement-detail'),
    url(r'^advertisement-edit/(?P<slug>[-\w]+)/$', AdvertisementEditView.as_view(), name='advertisement-edit'),
    url(r'^advertisement-delete/(?P<slug>[-\w]+)/$', AdvertisementDeleteView.as_view(), name='advertisement-delete'),
    url(r'^category-listing/(?P<slug>[-\w]+)/$', CategoryListingView.as_view(), name='category-listing'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        AccountActivationView.as_view(), name='activate'),
    url(r'^like-ad/(?P<slug>[-\w]+)/$', LikeView.as_view(), name='like-ad'),
    url(r'^pay/(?P<slug>[-\w]+)/$', PayView.as_view(), name='pay'),
    url(r'^search/$', SearchAdView.as_view(), name='search'),
    url(r'^expired/$', InactiveLinkView.as_view(), name='expired'),
]