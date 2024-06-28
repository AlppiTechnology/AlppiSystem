#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import CTCIInternalNote
from apps.ct_requests.ct_ci_internal_note.serializer import CTCIInternalNoteSerializer


logger = logging.getLogger('django')


class BaseCTCIInternalNote():

    def get_object(self, pk) -> tuple:
        try:
            return (CTCIInternalNote.objects.get(pk=pk), None)
        except CTCIInternalNote.DoesNotExist:
            message = 'Não foi possivel encontrar este CTCIInternalNote.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (CTCIInternalNote.objects.all(), None)
        except CTCIInternalNote.DoesNotExist:
            message = 'Não foi possivel encontrar todos os CTCIInternalNote.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_ct_ci_internal_note_data(self, pk) -> tuple:
        """
            Captura os id da ct_ci_internal_note e dados serializados de um ct_ci_internal_note especifica
        """
        logger.info(f'Capturando dados do ct_ci_internal_note id:{pk}')
        ct_ci_internal_note_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = CTCIInternalNoteSerializer(ct_ci_internal_note_id)
        return ct_ci_internal_note_id, selrializer.data
