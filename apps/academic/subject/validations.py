#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

def validate_subject_name(data) -> bool:
    subject_name = data.get('subject_name')
    if not subject_name:
        raise ValidationError('Informe o nome da Disciplina')
    return True

def validate_subject_area(data) -> bool:
    subject_area = data.get('fk_subject_area')
    if not subject_area:
        raise ValidationError('Informe a Area do Conhecimento')
    return True