#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper

logger = logging.getLogger('django')


def validate_repeated_subject(pedagogical_list:list):
    """
        Verifica se há disciplinas repetidas na lista de informações pedagógicas de uma turma.

        Params:
            pedagogical_class_info (list): Uma lista de dicionários contendo informações pedagógicas sobre uma turma.

        Returns:
            str: Uma mensagem de erro se disciplinas repetidas forem encontradas. Caso contrário, retorna None.
    """
    
    logger.info('Verifica se há disciplinas repetidas na lista de informações pedagógicas de uma turma.')
    subjects = []
    for pedagogical in pedagogical_list:
        if pedagogical.get('fk_subject') in subjects:
            message = f'Não é possivel possível cadastrar a diciplina {pedagogical.get("fk_subject")} duas vezes na mesma turma. '\
                'Mude a disciplina deste professor ou desative a que está cadastrada para que possa inserir a nova.'

            return ResponseHelper.HTTP_400({'detail':message})
        subjects.append(pedagogical.get('fk_subject'))



def validate_pedagogical_updates(pedagogical_salved: list, pedagogical_edited:list):
    to_delete = []
    to_update = []
    to_add    = []

    # captura os ids dos dados existentes e dos que estão vindo para update
    existing_ids = [item.get("pk_pedagogical_setting") for item in pedagogical_salved ]
    editedes_ids = [item.get("pk_pedagogical_setting") for item in pedagogical_edited if item.get("pk_pedagogical_setting")]
    
    # Captura somente os pedagogical novos
    to_add = [item for item in pedagogical_edited if not item.get("pk_pedagogical_setting")]
    # Captura os pedagogical percistentes
    to_update = [item for item in pedagogical_edited if item.get("pk_pedagogical_setting")]

    for id in existing_ids:
        if id not in editedes_ids:
            to_delete.append(id)


    return to_delete, to_update, to_add

