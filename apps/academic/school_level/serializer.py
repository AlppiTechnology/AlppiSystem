from rest_framework import serializers
from apps.academic.models import SchoolLevel


class SchoolLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolLevel
        fields = '__all__'