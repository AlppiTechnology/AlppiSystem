#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import DRCTSeverity
from apps.ct_requests.drct_severiy.serializer import DRCTSeveritySerializer


logger = logging.getLogger('django')


class BaseDRCTSeverity():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTSeverity.objects.get(pk=pk), None)
        except DRCTSeverity.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTSeverity.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTSeverity.objects.all(), None)
        except DRCTSeverity.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTSeverity.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_severiy_data(self, pk) -> tuple:
        """
            Captura os id da drct_severiy e dados serializados de um drct_severiy especifica
        """
        logger.info(f'Capturando dados do drct_severiy id:{pk}')
        drct_severiy_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTSeveritySerializer(drct_severiy_id)
        return drct_severiy_id, selrializer.data
