from rest_framework import serializers
from apps.academic.models import PedagogicalSetting


class PedagogicalSettingSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='fk_class_setting.name', read_only=True, required=False)
    subject_name = serializers.CharField(source='fk_subject.name', read_only=True, required=False)
    employee_name = serializers.CharField(source='fk_employee_user.username', read_only=True, required=False)


    class Meta:
        model = PedagogicalSetting
        fields = [
            'pk_pedagogical_setting',
            'fk_class_setting',
            'class_name',
            'fk_subject',
            'subject_name',
            'fk_employee_user',
            'employee_name',
            'edited',
            'status'
            ]