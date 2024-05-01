from rest_framework import serializers
from apps.academic.models import SchoolYear


class SchoolYearSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='fk_campus.campus_name', read_only=True, required=False)
    term_type_name = serializers.CharField(source='pk_term_type.name', read_only=True, required=False)

    class Meta:
        model = SchoolYear
        fields = [
            'pk_school_year',
            'fk_campus',
            'campus_name',
            'fk_term_type',
            'term_type_name',
            'year',
            'total_grade',
            'average_grade',
            'created',
            'edited',
            'skill',
            'status',
        ]