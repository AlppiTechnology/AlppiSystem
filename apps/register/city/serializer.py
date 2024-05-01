#!/usr/bin/python
# -*- encoding: utf-8 -*-

from rest_framework import serializers
from apps.register.models import City

class CitySerializer(serializers.ModelSerializer):
    fu_name = serializers.CharField(source='fk_fu.fu_name', read_only=True, required=False)

    class Meta:
        model = City
        fields = [
            'pk_city',
            'city_name',
            'fk_fu',
            'fu_name'
        ]