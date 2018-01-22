from django.contrib import admin

from applications.advertisements.models import Advertisement, Category


admin.site.register(Advertisement)
admin.site.register(Category)