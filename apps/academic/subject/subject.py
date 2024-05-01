#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.academic.models import Subject
from apps.academic.subject.serializer import SubjectSerializer


logger = logging.getLogger('django')


class BaseSubject():

    def get_object(self, pk) -> tuple:
        try:
            return (Subject.objects.get(pk=pk), None)
        except Subject.DoesNotExist:
            message = 'Não foi possivel encontrar este Subject.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (Subject.objects.all(), None)
        except Subject.DoesNotExist:
            message = 'Não foi possivel encontrar todos os Subject.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_subject_data(self, pk) -> tuple:
        """
            Captura os id da subject e dados serializados de um subject especifica
        """
        logger.info(f'Capturando dados do subject id:{pk}')
        subject_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = SubjectSerializer(subject_id)
        return subject_id, selrializer.data
