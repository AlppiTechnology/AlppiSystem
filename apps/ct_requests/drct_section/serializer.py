from rest_framework import serializers
from apps.ct_requests.models import DRCTSection

class DRCTSectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DRCTSection
        fields = [
            'pk_drct_section',
            'fk_drct_chapter',
            'name'
        ]