from rest_framework import serializers
from apps.academic.models import StudentPresence


class StudentPresenceSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='fk_class.name', read_only=True, required=False)
    term_name = serializers.CharField(source='fk_term.name', read_only=True, required=False)
    subject_name = serializers.CharField(source='fk_subject.subject_name', read_only=True, required=False)
    student_name = serializers.CharField(source='fk_student_user.username', read_only=True, required=False)
    registration = serializers.CharField(source='fk_student_user.registration', read_only=True, required=False)


    class Meta:
        model = StudentPresence
        fields = [
            'pk_student_presence',
            'fk_class',
            'class_name',
            'fk_term',
            'term_name',
            'fk_subject',
            'subject_name',
            'fk_student_user',
            'student_name',
            'registration',
            'presence',
            'date_presence'
            ]
        

class StudentPresenceCreateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='fk_student_user.username', read_only=True, required=False)
    registration = serializers.CharField(source='fk_student_user.registration', read_only=True, required=False)


    class Meta:
        model = StudentPresence
        fields = [
            'pk_student_presence',
            'fk_class',
            'fk_term',
            'fk_subject',
            'fk_student_user',
            'student_name',
            'registration',
            'presence',
            'date_presence'
            ]