#!/usr/bin/python
# -*- encoding: utf-8 -*-

from rest_framework import serializers
from apps.register.models import User

class StudentSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='fk_city.city_name', read_only=True, required=False)
    fu_name = serializers.CharField(source='fk_fu.fu_name', read_only=True, required=False)
    campus_name = serializers.CharField(source='fk_campus.campus_name', read_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'pk_user',
            'registration',
            'username',
            'cpf',
            'password',
            'fk_campus',
            'campus_name',
            'phone',
            'email',
            'fk_city',
            'city_name',
            'fk_fu',
            'fu_name',
            'sex',
            'birth_date',
            'created',
            'edited',
            'last_login',
            'is_superuser',
            'is_staff',
            'is_active',
        ]