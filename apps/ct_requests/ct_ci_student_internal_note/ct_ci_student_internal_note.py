#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
from datetime import datetime

from alppi.responses import ResponseHelper
from apps.ct_requests.models import CTCIStudentInternalNote
from apps.ct_requests.ct_ci_student_internal_note.serializer import CTCIStudentInternalNoteSerializer


logger = logging.getLogger('django')


class BaseCTCIStudentInternalNote():

    def get_object(self, pk) -> tuple:
        try:
            return (CTCIStudentInternalNote.objects.get(pk=pk), None)
        except CTCIStudentInternalNote.DoesNotExist:
            message = 'Não foi possivel encontrar este CTCIStudentInternalNote.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (CTCIStudentInternalNote.objects.all(), None)
        except CTCIStudentInternalNote.DoesNotExist:
            message = 'Não foi possivel encontrar todos os CTCIStudentInternalNote.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_ct_ci_student_internal_note_data(self, pk) -> tuple:
        """
            Captura os id da ct_ci_student_internal_note e dados serializados de um ct_ci_student_internal_note especifica
        """
        logger.info(f'Capturando dados do ct_ci_student_internal_note id:{pk}')
        ct_ci_student_internal_note_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = CTCIStudentInternalNoteSerializer(ct_ci_student_internal_note_id)
        return ct_ci_student_internal_note_id, selrializer.data
    
    def create_pct_ci_student_internal_note(self, internal_note:int, students:list):
        try:
            # verifica se existe disciplinas repetidas
            students = set(students)

            for student in students:
                data = {}
                data['fk_ct_ci_internal_note'] = internal_note
                data['fk_student'] = student

                serializer = CTCIStudentInternalNoteSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                else:
                    return  (None, ResponseHelper.HTTP_404({'detail': serializer.errors}))
            return None, None

        except CTCIStudentInternalNote.DoesNotExist:
            message = 'Não foi possivel encontrar todos os CTCIStudentInternalNote.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))
