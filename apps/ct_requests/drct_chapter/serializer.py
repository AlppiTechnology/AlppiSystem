from rest_framework import serializers
from apps.ct_requests.models import DRCTChapter

class DRCTChapterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DRCTChapter
        fields = [
            'pk_drct_chapter',
            'name'
        ]