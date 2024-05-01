#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper

from apps.register.models import Campus
from apps.register.campus.serializer import CampusSerializer


logger = logging.getLogger('django')


class BaseCampus():

    def get_object(self, pk) -> tuple:
        try:
            return (Campus.objects.get(pk=pk), None)
        except Campus.DoesNotExist:
            message = 'Não foi possivel encontrar este Campus.'
            logger.error({'results': message})
            return None, ResponseHelper.HTTP_404({'results': message})

    def get_all_object(self) -> tuple:
        try:
            return (Campus.objects.all(), None)
        except Campus.DoesNotExist:
            message = 'Não foi possivel encontrar todos os Campus.'
            logger.error({'results': message})
            return None, ResponseHelper.HTTP_404({'results': message})


    def get_campus_data(self, pk) -> dict:
        """
            Captura os id da campus e dados serializados de uma campus especifica
        """
        logger.info(f'Capturando dados do campus id:{pk}')
        campus_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = CampusSerializer(campus_id)
        return campus_id, selrializer.data
