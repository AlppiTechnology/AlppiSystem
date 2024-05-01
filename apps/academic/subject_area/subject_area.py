#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.academic.models import SubjectArea
from apps.academic.subject_area.serializer import SubjectAreaSerializer


logger = logging.getLogger('django')


class BaseSubjectArea():

    def get_object(self, pk) -> tuple:
        try:
            return (SubjectArea.objects.get(pk=pk), None)
        except SubjectArea.DoesNotExist:
            message = 'Não foi possivel encontrar este SubjectArea.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (SubjectArea.objects.all(), None)
        except SubjectArea.DoesNotExist:
            message = 'Não foi possivel encontrar todos os SubjectArea.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_subject_area_data(self, pk) -> tuple:
        """
            Captura os id da subject_area e dados serializados de um subject_area especifica
        """
        logger.info(f'Capturando dados do subject_area id:{pk}')
        subject_area_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = SubjectAreaSerializer(subject_area_id)
        return subject_area_id, selrializer.data
