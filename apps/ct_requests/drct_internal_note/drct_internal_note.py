#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import DRCTInternalNote
from apps.ct_requests.drct_internal_note.serializer import DRCTInternalNoteSerializer


logger = logging.getLogger('django')


class BaseDRCTInternalNote():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTInternalNote.objects.get(pk=pk), None)
        except DRCTInternalNote.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTInternalNote.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTInternalNote.objects.all(), None)
        except DRCTInternalNote.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTInternalNote.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_internal_note_data(self, pk) -> tuple:
        """
            Captura os id da drct_internal_note e dados serializados de um drct_internal_note especifica
        """
        logger.info(f'Capturando dados do drct_internal_note id:{pk}')
        drct_internal_note_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTInternalNoteSerializer(drct_internal_note_id)
        return drct_internal_note_id, selrializer.data
