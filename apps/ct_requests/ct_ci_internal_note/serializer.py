from rest_framework import serializers
from apps.ct_requests.models import CTCIInternalNote

class CTCIInternalNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = CTCIInternalNote
        fields = [
            'pk_ct_ci_internal_note',
            'title',
            'fk_reporter',
            'fk_campus',
            'ct_ci_single_attach',
            'ct_ci_deadline',
            'ct_ci_student_deadline',
            'ct_ci_cal_statement',
            'ct_ci_cmdt_statement',
            'ct_ci_cmdt_answer',
            'created',
            'updated',
            'status'
        ]