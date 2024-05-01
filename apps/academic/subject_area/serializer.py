#!/usr/bin/python
# -*- encoding: utf-8 -*-

from rest_framework import serializers
from apps.academic.models import SubjectArea

class SubjectAreaSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='fk_campus.campus_name', read_only=True, required=False)

    class Meta:
        model = SubjectArea
        fields = [
            'pk_subject_area',
            'fk_campus',
            'campus_name',
            'name',
            'created',
            'edited',
            'status'
        ]