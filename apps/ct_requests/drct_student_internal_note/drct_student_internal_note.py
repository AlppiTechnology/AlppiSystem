#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
from datetime import datetime

from alppi.responses import ResponseHelper
from apps.ct_requests.models import DRCTStudentInternalNote
from apps.ct_requests.drct_student_internal_note.serializer import DRCTStudentInternalNoteSerializer


logger = logging.getLogger('django')


class BaseDRCTStudentInternalNote():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTStudentInternalNote.objects.get(pk=pk), None)
        except DRCTStudentInternalNote.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTStudentInternalNote.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTStudentInternalNote.objects.all(), None)
        except DRCTStudentInternalNote.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTStudentInternalNote.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_student_internal_note_data(self, pk) -> tuple:
        """
            Captura os id da drct_student_internal_note e dados serializados de um drct_student_internal_note especifica
        """
        logger.info(f'Capturando dados do drct_student_internal_note id:{pk}')
        drct_student_internal_note_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTStudentInternalNoteSerializer(drct_student_internal_note_id)
        return drct_student_internal_note_id, selrializer.data
    
    def create_pdrct_student_internal_note(self, internal_note:int, students:list):
        try:
            # verifica se existe disciplinas repetidas
            students = set(students)

            for student in students:
                data = {}
                data['fk_drct_internal_note'] = internal_note
                data['fk_student'] = student

                serializer = DRCTStudentInternalNoteSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                else:
                    return  (None, ResponseHelper.HTTP_404({'detail': serializer.errors}))
            return None, None

        except DRCTStudentInternalNote.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTStudentInternalNote.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))
