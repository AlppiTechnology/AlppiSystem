#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

def validate_subject_area_name(data) -> bool:
    name = data.get('name').strip()
    if not name:
        raise ValidationError('Informe o nome da Area do Conhecimento')
    return True