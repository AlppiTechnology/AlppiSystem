from rest_framework import serializers
from apps.ct_requests.models import DRCTSeverity

class DRCTSeveritySerializer(serializers.ModelSerializer):

    class Meta:
        model = DRCTSeverity
        fields = [
            'pk_drct_severity',
            'name'
        ]