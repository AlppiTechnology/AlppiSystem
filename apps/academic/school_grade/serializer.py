from rest_framework import serializers
from apps.academic.models import SchoolGrade


class SchoolGradeSerializer(serializers.ModelSerializer):
    school_level = serializers.CharField(source='fk_school_level.name', read_only=True, required=False)
    class Meta:
        model = SchoolGrade
        fields = [
            'pk_school_grade',
            'name',
            'fk_school_level',
            'school_level'
        ]