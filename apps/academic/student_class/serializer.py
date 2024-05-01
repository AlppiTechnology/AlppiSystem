from rest_framework import serializers
from apps.academic.models import StudentClass


class StudentClassSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='fk_class_setting.name', read_only=True, required=False)
    student_name = serializers.CharField(source='fk_student_user.username', read_only=True, required=False)


    class Meta:
        model = StudentClass
        fields = [
            'pk_student_class',
            'fk_class_setting',
            'class_name',
            'fk_student_user',
            'student_name',
            'status'
            ]