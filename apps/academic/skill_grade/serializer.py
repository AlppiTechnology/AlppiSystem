from rest_framework import serializers
from apps.academic.models import SkillGrade


class SkillGradeSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='fk_class.name', read_only=True, required=False)
    term_name = serializers.CharField(source='fk_term.name', read_only=True, required=False)
    subject_name = serializers.CharField(source='fk_subject.subject_name', read_only=True, required=False)
    label_name = serializers.CharField(source='fk_skill.label_name', read_only=True, required=False)
    student_name = serializers.CharField(source='fk_student_user.username', read_only=True, required=False)
    registration = serializers.CharField(source='fk_student_user.registration', read_only=True, required=False)


    class Meta:
        model = SkillGrade
        fields = [
            'pk_skill_grade',
            'fk_class',
            'class_name',
            'fk_term',
            'term_name',
            'fk_subject',
            'subject_name',
            'fk_skill',
            'label_name',
            'fk_student_user',
            'student_name',
            'registration',
            'grade_1',
            'grade_2',
            'grade_3',
            'grade_4',
            'grade_5',
            'edited',
            'status',
            ]
        

class SkillGradeCreateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='fk_student_user.username', read_only=True, required=False)
    registration = serializers.CharField(source='fk_student_user.registration', read_only=True, required=False)


    class Meta:
        model = SkillGrade
        fields = [
            'pk_skill_grade',
            'fk_class',
            'fk_term',
            'fk_subject',
            'fk_skill',
            'fk_student_user',
            'student_name',
            'registration',
            'grade_1',
            'grade_2',
            'grade_3',
            'grade_4',
            'grade_5',
            'edited',
            'status'
            ]