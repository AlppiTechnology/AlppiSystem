#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper

logger = logging.getLogger('django')


def validate_repeated_regulaments(regulaments:list):

    logger.info('Verifica se há regulamentos repetidas na lista.')
    regulament = []
