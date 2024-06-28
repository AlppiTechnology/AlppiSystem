#!/usr/bin/python
# -*- encoding: utf-8 -*-
from datetime import datetime
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.ct_ci_regulament.validations import validate_repeated_regulaments
from apps.ct_requests.models import CTCIRegulament
from apps.ct_requests.ct_ci_regulament.serializer import CTCIRegulamentSerializer


logger = logging.getLogger('django')


class BaseCTCIRegulament():

    def get_object(self, pk) -> tuple:
        try:
            return (CTCIRegulament.objects.get(pk=pk), None)
        except CTCIRegulament.DoesNotExist:
            message = 'Não foi possivel encontrar este CTCIRegulament.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (CTCIRegulament.objects.all(), None)
        except CTCIRegulament.DoesNotExist:
            message = 'Não foi possivel encontrar todos os CTCIRegulament.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_ct_ci_regulament_data(self, pk) -> tuple:
        """
            Captura os id da ct_ci_regulament e dados serializados de um ct_ci_regulament especifica
        """
        logger.info(f'Capturando dados do ct_ci_regulament id:{pk}')
        ct_ci_regulament_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = CTCIRegulamentSerializer(ct_ci_regulament_id)
        return ct_ci_regulament_id, selrializer.data
    
    def create_pct_ci_regulament(self, internal_note:int, regulaments:list):
        try:
             # verifica se existe disciplinas repetidas
            repeated_subject = validate_repeated_regulaments(regulaments)
            if repeated_subject:
                return None, repeated_subject

            for regulament in regulaments:
                data = {}
                data['fk_ct_ci_internal_note'] = internal_note
                data['regulament'] = regulament

                serializer = CTCIRegulamentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                else:
                    return  (None, ResponseHelper.HTTP_404({'detail': serializer.errors}))
            return None, None

        except CTCIRegulament.DoesNotExist:
            message = 'Não foi possivel encontrar todos os CTCIRegulament.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))
