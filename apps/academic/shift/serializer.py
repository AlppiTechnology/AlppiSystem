from rest_framework import serializers
from apps.academic.models import Shift

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'