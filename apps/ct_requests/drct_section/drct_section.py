#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import DRCTSection
from apps.ct_requests.drct_section.serializer import DRCTSectionSerializer


logger = logging.getLogger('django')


class BaseDRCTSection():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTSection.objects.get(pk=pk), None)
        except DRCTSection.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTSection.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTSection.objects.all(), None)
        except DRCTSection.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTSection.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_section_data(self, pk) -> tuple:
        """
            Captura os id da drct_section e dados serializados de um drct_section especifica
        """
        logger.info(f'Capturando dados do drct_section id:{pk}')
        drct_section_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTSectionSerializer(drct_section_id)
        return drct_section_id, selrializer.data
