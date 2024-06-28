from rest_framework import serializers
from apps.ct_requests.models import CTCIComment

class CTCICommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CTCIComment
        fields = [
            'pk_ct_ci_comment',
            'fk_ct_ci_internal_note',
            'fk_user',
            'date',
            'comment'
            ]