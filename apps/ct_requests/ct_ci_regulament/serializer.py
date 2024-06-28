from rest_framework import serializers
from apps.ct_requests.models import CTCIRegulament

class CTCIRegulamentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CTCIRegulament
        fields = [
            'pk_ct_ci_regulament',
            'fk_ct_ci_internal_note',
            'regulament'
        ]