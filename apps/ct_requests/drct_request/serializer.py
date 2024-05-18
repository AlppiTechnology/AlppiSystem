from rest_framework import serializers
from apps.ct_requests.models import DRCTRequest

class DRCTRequestSerializer(serializers.ModelSerializer):
    term_type = serializers.CharField(source='fk_term_type.name', read_only=True, required=False)

    class Meta:
        model = DRCTRequest
        fields = [
            'pk_drct_request',
            'title',
            'fk_reporter',
            'fk_campus',
            'fk_drct_severity',
            'fk_drct_penalty',
            'fk_drct_chapter',
            'fk_drct_section',
            'fk_drct_paragraph',
            'date',
            'status'
        ]