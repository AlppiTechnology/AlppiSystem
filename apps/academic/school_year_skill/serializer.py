from rest_framework import serializers
from apps.academic.models import SchoolYearSkill


class SchoolYearSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='fk_skill.label_name', read_only=True, required=False)
    year = serializers.CharField(source='fk_school_year.year', read_only=True, required=False)


    class Meta:
        model = SchoolYearSkill
        fields = [
            'pk_school_year_skill',
            'fk_skill',
            'skill_name',
            'fk_school_year',
            'year'
        ]