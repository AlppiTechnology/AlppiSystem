from rest_framework import serializers
from apps.ct_requests.models import DRCTStudentRequest

class DRCTStudentRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DRCTStudentRequest
        fields = [
            'pk_drct_student_request',
            'fk_drct_request',
            'fk_student'
            ]