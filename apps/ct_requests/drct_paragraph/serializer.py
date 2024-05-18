from rest_framework import serializers
from apps.ct_requests.models import DRCTParagraph

class DRCTParagraphSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DRCTParagraph
        fields = [
            'pk_drct_paragraph',
            'fk_drct_section',
            'name',
            'value'
        ]