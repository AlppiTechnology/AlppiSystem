#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from alppi.responses import ResponseHelper

logger = logging.getLogger('django')


def validate_repeated_student(student_class:list):
    """
        Verifica se há alunos repetidos na lista de estudentes em uma turma.

        Esta função recebe uma lista de dicionários representando a configuração de uma turma, onde cada dicionário
        contém informações sobre um estudente. A função verifica se há alunos repetidos na lista com base no valor da chave
        'student' em cada dicionário. Se um aluno for encontrado mais de uma vez, a função retorna uma mensagem de erro
        indicando que não é possível cadastrar o mesmo aluno duas vezes na mesma turma.

        Params:
            student_class (list): Uma lista de dicionários contendo informações sobre os estudentes da turma.

        Returns:
            JsonResponse: Uma resposta JSON que inclui uma mensagem de erro e um código de resposta HTTP 400 (Bad Request)
            se alunos repetidos forem encontrados. Caso contrário, retorna None.

    """
    logger.info('Verifica se há alunos repetidos na lista de estudentes')
    students = []
    for student in student_class:
        if student in students:
            message = f'Não é possivel possível cadastrar o aluno {student} duas vezes na mesma turma. '

            return ResponseHelper.HTTP_400({'detail':message})
        students.append(student)

def validate_students_update(student_salved:list, student_edited:list):
    to_delete = []
    to_add    = []

    # captura o id dos alunos existentes na turma
    existing_ids = [item.get('fk_student_user') for item in student_salved]

    to_add = [item for item in student_edited if item not in existing_ids]

    to_delete = [item.get('pk_student_class') for item in student_salved 
                 if item.get('fk_student_user') not in student_edited]
    
    return to_delete, to_add