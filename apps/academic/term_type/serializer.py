from rest_framework import serializers
from apps.academic.models import TermType

class TermTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermType
        fields = '__all__'