#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper

logger = logging.getLogger('django')


def validate_repeated_regulaments(regulaments:list):

    logger.info('Verifica se há regulamentos repetidas na lista.')
    regulament_list = []
    for regulament in regulaments:
        if regulament in regulament_list:
            message = f"não é possovel cadastrar duas vezes o mesmo regulamento. {regulament}"
            return ResponseHelper.HTTP_400({'detail':message})
        
        regulament_list.append(regulament)