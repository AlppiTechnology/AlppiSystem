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

from datetime import datetime, date

def validate_chosen_date(chosen_date: str):
    """
    Valida se a data escolhida é anterior ou igual à data atual.

    Args:
        chosen_date (str): A data escolhida no formato 'YYYY-MM-DD'.

    Returns:
        tuple: Um tuple contendo a data escolhida como objeto de data e None se a data for válida,
               ou None e uma resposta de erro HTTP 400 se a data for inválida.
    """
    try:
        # Converte a string chosen_date em um objeto de data
        chosen_date = datetime.strptime(chosen_date, '%Y-%m-%d').date()

        if chosen_date > date.today():
            message = 'Não é autorizado aplicar presença a datas posteriores à atual'
            return ResponseHelper.HTTP_400({'detail': message})

    except ValueError:
        message = 'Formato de data inválido. O formato esperado é "YYYY-MM-DD".'
        return ResponseHelper.HTTP_400({'detail': message})
