#!/usr/bin/python
# -*- encoding: utf-8 -*-
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from alppi.responses import ResponseHelper


def validate_employee_visualisation(pedagogical_setting, user_id):
    """
    verifica se o usuario é o professor da turma para 
    poder vlsualizar as notas da turma
    """

    if pedagogical_setting.get('fk_employee_user') != user_id:
        message = f'Este usuario não é autorizado a ver as notas desta disciplina!.'
        return ResponseHelper.HTTP_400({'detail': message})


def validate_term_date(school_year_date):
    """
    Verifica se a data atual esta etre a data do term. Caso não esteja
    não pode ser autorizado a criação de novas novas

    Args:
        school_year_date (dict): dicionário contendo as informações de datas do term escolhido

    Returns:
        bool: True or False
    """

    return True if school_year_date.get('init_date') <= date.today() <= \
        school_year_date.get('final_date') else False


def valeidate_sum_grades(grade, term_grade):
    """
    Verifica se a soma dos valores das chaves que começam com 'grade' é menor ou igual a 20.

    Args:
        dicionario (dict): Um dicionário onde as chaves representam os índices e os valores são os valores associados a esses índices.

    Returns:
        bool: True se a soma dos valores das chaves que começam com 'grade' for menor ou igual a 20, False caso contrário.
    """
    sum_grade = sum(valor for chave, valor in grade.items()
               if chave.startswith("grade_")) > term_grade
    
    if sum_grade:
        message = f'A soma das notas do aluno {grade.get("student_name")} não podem passar de {term_grade}. '\
        'Verifique as notas e envie novamente.'
        return ResponseHelper.HTTP_400({'detail': message})