from rest_framework import serializers
from apps.ct_requests.models import DRCTPenalty

class DRCTPenaltySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DRCTPenalty
        fields = [
            'pk_drct_penalty',
            'name'
        ]