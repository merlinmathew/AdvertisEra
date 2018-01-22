from django.contrib import admin

from applications.contacts.models import Contact, AdvertiseraAddress


admin.site.register(Contact)
admin.site.register(AdvertiseraAddress)
