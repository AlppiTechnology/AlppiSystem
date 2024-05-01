from rest_framework import serializers
from apps.academic.models import SchoolYearDate


class SchoolYearDateSerializer(serializers.ModelSerializer):
    term_name = serializers.CharField(source='fk_term.name', read_only=True, required=False)

    class Meta:
        model = SchoolYearDate
        fields = [
            'pk_school_year_date',
            'fk_school_year',
            'fk_term',
            'term_name',
            'grade',
            'init_date',
            'final_date'
        ]