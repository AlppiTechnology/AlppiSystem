#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

def validate_label_name(data) -> bool:
    label_name = data.get('label_name')
    if not label_name:
        raise ValidationError('Informe o nome da Disciplina')
    return True

def validate_description(data) -> bool:
    description = data.get('description')
    if not description:
        raise ValidationError('Informe a Area do Conhecimento')
    return True