from rest_framework import serializers
from apps.ct_requests.models import DRCTComment

class DRCTCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DRCTComment
        fields = [
            'pk_drct_comment',
            'fk_drct_internal_note',
            'fk_user',
            'date',
            'comment'
            ]