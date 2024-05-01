#!/usr/bin/python
# -*- encoding: utf-8 -*-

from rest_framework import serializers
from apps.academic.models import SkillSettings

class SkillSettingsSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='fk_campus.campus_name', read_only=True, required=False)

    class Meta:
        model = SkillSettings
        fields = [
            'pk_skill_setting',
            'fk_campus',
            'campus_name',
            'label_name',
            'description',
            'status'
        ]