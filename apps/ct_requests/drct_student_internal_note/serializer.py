from rest_framework import serializers
from apps.ct_requests.models import DRCTStudentInternalNote

class DRCTStudentInternalNoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DRCTStudentInternalNote
        fields = [
            'pk_drct_student_internal_note',
            'fk_drct_internal_note',
            'fk_student'
            ]