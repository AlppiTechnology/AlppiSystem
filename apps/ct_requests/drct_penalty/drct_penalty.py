#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import DRCTPenalty
from apps.ct_requests.drct_penalty.serializer import DRCTPenaltySerializer


logger = logging.getLogger('django')


class BaseDRCTPenalty():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTPenalty.objects.get(pk=pk), None)
        except DRCTPenalty.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTPenalty.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTPenalty.objects.all(), None)
        except DRCTPenalty.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTPenalty.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_penalty_data(self, pk) -> tuple:
        """
            Captura os id da drct_penalty e dados serializados de um drct_penalty especifica
        """
        logger.info(f'Capturando dados do drct_penalty id:{pk}')
        drct_penalty_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTPenaltySerializer(drct_penalty_id)
        return drct_penalty_id, selrializer.data
