from rest_framework import serializers
from apps.ct_requests.models import CTCIStudentInternalNote

class CTCIStudentInternalNoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CTCIStudentInternalNote
        fields = [
            'pk_ct_ci_student_internal_note',
            'fk_ct_ci_internal_note',
            'fk_student'
            ]