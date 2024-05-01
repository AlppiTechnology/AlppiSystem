from rest_framework import serializers
from apps.academic.models import SchoolGrade


class SchoolGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGrade
        fields = '__all__'