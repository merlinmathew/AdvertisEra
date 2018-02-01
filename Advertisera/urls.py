"""Advertisera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from applications.advertisements.views import HomeView
from django.conf import settings
from django.conf.urls import url,include
from django.contrib import admin
from django.utils.functional import curry
from django.views import static
from django.views.defaults import permission_denied, page_not_found, server_error


urlpatterns = [
    url(r'^advertisera-admin/', admin.site.urls),
    url(r'^', include('applications.advertisements.urls')),
    url(r'^contact', include('applications.contacts.urls')),
    url(r'^advertisera-password/', include('password_reset.urls')),
    url(r'^media/(?P<path>.*)$', static.serve,{'document_root': settings.MEDIA_ROOT,}),
]

handler403 = curry(permission_denied, template_name='403.html')
handler404 = curry(page_not_found, template_name='404.html')
handler500 = curry(server_error, template_name='500.html')

admin.site.site_header = 'Advert!sera Administration'
admin.site.site_title = 'Advert!sera Site Admin'
admin.site.index_title = 'Advert!sera Site Admin'
