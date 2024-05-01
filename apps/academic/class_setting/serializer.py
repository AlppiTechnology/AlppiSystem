from rest_framework import serializers
from apps.academic.models import ClassSetting


class ClassSettingSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='fk_campus.campus_name', read_only=True, required=False)
    school_grade_name = serializers.CharField(source='fk_school_grade.name', read_only=True, required=False)
    shift_name = serializers.CharField(source='fk_shift.name', read_only=True, required=False)
    school_year_name = serializers.CharField(source='fk_school_year.year', read_only=True, required=False)



    class Meta:
        model = ClassSetting
        fields = [
            'pk_class_setting',
            'fk_campus',
            'campus_name',
            'fk_school_grade',
            'school_grade_name',
            'fk_shift',
            'shift_name',
            'fk_school_year',
            'school_year_name',
            'name',
            'edited',
            'skill',
            'status',
        ]