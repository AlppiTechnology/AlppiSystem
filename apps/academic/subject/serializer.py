#!/usr/bin/python
# -*- encoding: utf-8 -*-

from rest_framework import serializers
from apps.academic.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='fk_campus.campus_name', read_only=True, required=False)

    class Meta:
        model = Subject
        fields = [
            'pk_subject',
            'fk_campus',
            'campus_name',
            'fk_subject_area',
            'subject_code',
            'subject_name',
            'created',
            'edited',
            'status'
        ]