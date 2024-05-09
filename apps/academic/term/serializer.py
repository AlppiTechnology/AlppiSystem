from rest_framework import serializers
from apps.academic.models import Term

class TermSerializer(serializers.ModelSerializer):
    term_type = serializers.CharField(source='fk_term_type.name', read_only=True, required=False)

    class Meta:
        model = Term
        fields = [
            'pk_term_type',
            'fk_term_type',
            'name',
            'term_type'
        ]