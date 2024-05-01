#!/usr/bin/python
# -*- encoding: utf-8 -*-

from rest_framework import serializers
from apps.register.models import Campus

class CampusSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='fk_city.city_name', read_only=True, required=False)
    fu_name = serializers.CharField(source='fk_fu.fu_name', read_only=True, required=False)

    class Meta:
        model = Campus
        fields = [
            'pk_campus',
            'cnpj',
            'campus_code',
            'campus_name',
            'trading_name',
            'company_name',
            'public_place',
            'fk_city',
            'city_name',
            'fk_fu',
            'fu_name',
            'email',
            'phone',
            'created',
            'edited',
            'status'
        ]