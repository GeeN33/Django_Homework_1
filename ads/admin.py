from django.contrib import admin

from ads.models import Categories, Location, Users, Ad
# Register your models here.

admin.site.register(Categories)

admin.site.register(Location)

admin.site.register(Users)

admin.site.register(Ad)