#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.academic.models import SchoolLevel
from apps.academic.school_level.serializer import SchoolLevelSerializer


logger = logging.getLogger('django')


class BaseSchoolLevel():

    def get_object(self, pk) -> tuple:
        try:
            return (SchoolLevel.objects.get(pk=pk), None)
        except SchoolLevel.DoesNotExist:
            message = 'Não foi possivel encontrar este SchoolLevel.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (SchoolLevel.objects.all(), None)
        except SchoolLevel.DoesNotExist:
            message = 'Não foi possivel encontrar todos os SchoolLevel.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_school_level_data(self, pk) -> tuple:
        """
            Captura os id da school_level e dados serializados de um school_level especifica
        """
        logger.info(f'Capturando dados do school_level id:{pk}')
        school_level_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = SchoolLevelSerializer(school_level_id)
        return school_level_id, selrializer.data
