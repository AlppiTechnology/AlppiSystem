from rest_framework import serializers
from apps.ct_requests.models import DRCTRegulament

class DRCTRegulamenterializer(serializers.ModelSerializer):
    
    class Meta:
        model = DRCTRegulament
        fields = [
            'pk_ctrd_regulament',
            'fk_internal_note',
            'regulament'
        ]