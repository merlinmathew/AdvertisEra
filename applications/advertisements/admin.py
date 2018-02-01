from django.contrib import admin

from applications.advertisements.models import Advertisement, Category

class AdvertisementAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()

admin.site.register(Advertisement,AdvertisementAdmin)
admin.site.register(Category)