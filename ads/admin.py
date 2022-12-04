from django.contrib import admin

from ads.models import Categories, Location, Ad
# Register your models here.

admin.site.register(Categories)

admin.site.register(Location)

admin.site.register(Ad)