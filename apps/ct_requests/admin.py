from django.contrib import admin

from apps.ct_requests.models import *
# Register your models here.

admin.site.register(CTRDSeverity)
admin.site.register(CTRDPenalty)
admin.site.register(CTRDChapter)
admin.site.register(CTRDParagraph)
admin.site.register(CTRDStudentRequest)
admin.site.register(CTRDComment)