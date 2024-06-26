from rest_framework import serializers
from apps.ct_requests.models import DRCTInternalNote

class DRCTInternalNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = DRCTInternalNote
        fields = [
            'pk_drct_internal_note',
            'title',
            'fk_reporter',
            'fk_campus',
            'drct_single_attach',
            'ctdr_deadline',
            'ctdr_student_deadline',
            'ctdr_cal_statement',
            'ctdr_cmdt_statement',
            'ctdr_cmdt_answer',
            'created',
            'updated',
            'status'
        ]