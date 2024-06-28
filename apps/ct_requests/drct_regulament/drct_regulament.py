#!/usr/bin/python
# -*- encoding: utf-8 -*-
from datetime import datetime
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.drct_regulament.validations import validate_repeated_regulaments
from apps.ct_requests.models import DRCTRegulament
from apps.ct_requests.drct_regulament.serializer import DRCTRegulamenterializer


logger = logging.getLogger('django')


class BaseDRCTRegulament():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTRegulament.objects.get(pk=pk), None)
        except DRCTRegulament.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTRegulament.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTRegulament.objects.all(), None)
        except DRCTRegulament.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTRegulament.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_regulament_data(self, pk) -> tuple:
        """
            Captura os id da drct_regulament e dados serializados de um drct_regulament especifica
        """
        logger.info(f'Capturando dados do drct_regulament id:{pk}')
        drct_regulament_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTRegulamenterializer(drct_regulament_id)
        return drct_regulament_id, selrializer.data
    
    def create_pdrct_regulament(self, internal_note:int, regulaments:list):
        try:
             # verifica se existe disciplinas repetidas
            repeated_subject = validate_repeated_regulaments(regulaments)
            if repeated_subject:
                return None, repeated_subject

            for regulament in regulaments:
                data = {}
                data['fk_drct_internal_note'] = internal_note
                data['regulament'] = regulament

                serializer = DRCTRegulamenterializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                else:
                    return  (None, ResponseHelper.HTTP_404({'detail': serializer.errors}))
            return None, None

        except DRCTRegulament.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTRegulament.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))
