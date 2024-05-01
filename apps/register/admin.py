from django.contrib import admin

from apps.register.models import *

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ("groups",)

admin.site.register(FederativeUnit)
admin.site.register(City)
admin.site.register(Campus)
admin.site.register(User, ProfileAdmin)