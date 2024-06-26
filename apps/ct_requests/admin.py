from django.contrib import admin

from apps.ct_requests.models import *
# Register your models here.

admin.site.register(DRCTInternalNote)
admin.site.register(DRCTRegulament)
admin.site.register(DRCTStudentInternalNote)
admin.site.register(DRCTComment)