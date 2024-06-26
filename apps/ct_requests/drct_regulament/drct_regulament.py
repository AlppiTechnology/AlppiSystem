#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
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
