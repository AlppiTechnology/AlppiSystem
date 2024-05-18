from django.contrib import admin

from apps.ct_requests.models import *
# Register your models here.

admin.site.register(DRCTRequest)
admin.site.register(DRCTSeverity)
admin.site.register(DRCTPenalty)
admin.site.register(DRCTChapter)
admin.site.register(DRCTSection)
admin.site.register(DRCTParagraph)
admin.site.register(DRCTStudentRequest)
admin.site.register(DRCTComment)