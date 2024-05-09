#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.academic.models import TermType
from apps.academic.term_type.serializer import TermTypeSerializer


logger = logging.getLogger('django')


class BaseTermType():

    def get_object(self, pk) -> tuple:
        try:
            return (TermType.objects.get(pk=pk), None)
        except TermType.DoesNotExist:
            message = 'Não foi possivel encontrar este TermType.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (TermType.objects.all(), None)
        except TermType.DoesNotExist:
            message = 'Não foi possivel encontrar todos os TermType.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_term_type_data(self, pk) -> tuple:
        """
            Captura os id da term_type e dados serializados de um term_type especifica
        """
        logger.info(f'Capturando dados do term_type id:{pk}')
        term_type_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = TermTypeSerializer(term_type_id)
        return term_type_id, selrializer.data
