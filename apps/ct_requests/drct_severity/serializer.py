from rest_framework import serializers
from apps.ct_requests.models import DRCTSeverity

class DRCTSeveritySerializer(serializers.ModelSerializer):
    term_type = serializers.CharField(source='fk_term_type.name', read_only=True, required=False)

    class Meta:
        model = DRCTSeverity
        fields = [
            'pk_drct_severity',
            'name'
        ]