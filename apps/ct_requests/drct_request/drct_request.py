#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import DRCTRequest
from apps.ct_requests.drct_request.serializer import DRCTRequestSerializer


logger = logging.getLogger('django')


class BaseDRCTRequest():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTRequest.objects.get(pk=pk), None)
        except DRCTRequest.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTRequest.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTRequest.objects.all(), None)
        except DRCTRequest.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTRequest.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_request_data(self, pk) -> tuple:
        """
            Captura os id da drct_request e dados serializados de um drct_request especifica
        """
        logger.info(f'Capturando dados do drct_request id:{pk}')
        drct_request_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTRequestSerializer(drct_request_id)
        return drct_request_id, selrializer.data
