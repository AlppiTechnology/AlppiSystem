from django.contrib import admin

from apps.ct_requests.models import *
# Register your models here.

admin.site.register(CTCIInternalNote)
admin.site.register(CTCIRegulament)
admin.site.register(CTCIStudentInternalNote)
admin.site.register(CTCIComment)