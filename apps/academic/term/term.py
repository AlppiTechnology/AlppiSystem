#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.academic.models import Term
from apps.academic.term.serializer import TermSerializer


logger = logging.getLogger('django')


class BaseTerm():

    def get_object(self, pk) -> tuple:
        try:
            return (Term.objects.get(pk=pk), None)
        except Term.DoesNotExist:
            message = 'Não foi possivel encontrar este Term.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (Term.objects.all(), None)
        except Term.DoesNotExist:
            message = 'Não foi possivel encontrar todos os Term.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_term_data(self, pk) -> tuple:
        """
            Captura os id da term e dados serializados de um term especifica
        """
        logger.info(f'Capturando dados do term id:{pk}')
        term_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = TermSerializer(term_id)
        return term_id, selrializer.data
