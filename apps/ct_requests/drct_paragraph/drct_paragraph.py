#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import DRCTParagraph
from apps.ct_requests.drct_paragraph.serializer import DRCTParagraphSerializer


logger = logging.getLogger('django')


class BaseDRCTParagraph():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTParagraph.objects.get(pk=pk), None)
        except DRCTParagraph.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTParagraph.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTParagraph.objects.all(), None)
        except DRCTParagraph.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTParagraph.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_paragraph_data(self, pk) -> tuple:
        """
            Captura os id da drct_paragraph e dados serializados de um drct_paragraph especifica
        """
        logger.info(f'Capturando dados do drct_paragraph id:{pk}')
        drct_paragraph_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTParagraphSerializer(drct_paragraph_id)
        return drct_paragraph_id, selrializer.data
