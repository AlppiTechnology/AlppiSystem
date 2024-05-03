#!/usr/bin/python
# -*- encoding: utf-8 -*-
from datetime import datetime
import logging
from django.db.models import Q, F

from alppi.responses import ResponseHelper
from apps.academic.models import StudentPresence
from apps.academic.student_presence.serializer import StudentPresenceCreateSerializer, StudentPresenceSerializer


logger = logging.getLogger('django')


class BaseStudentPresence():

    def get_object(self, pk) -> tuple:
        try:
            return (StudentPresence.objects.get(pk=pk), None)
        except StudentPresence.DoesNotExist:
            message = 'Não foi possivel encontrar este StudentPresence.'
            logger.error({'results': message})
            return (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (StudentPresence.objects.all(), None)
        except StudentPresence.DoesNotExist:
            message = 'Não foi possivel encontrar todos os StudentPresence.'
            logger.error({'results': message})
            return (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_student_presence_data(self, pk) -> tuple:
        """
            Captura os id da student_presence e dados serializados de um student_presence especifica
        """
        logger.info(f'Capturando dados do student_presence id:{pk}')
        student_presence_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = StudentPresenceSerializer(student_presence_id)
        return student_presence_id, selrializer.data

    def get_students_presence(self, subject: int, class_id: int, 
                              term: int, chosen_date: str):

        query_result = StudentPresence.objects.filter(
            fk_student_user__studentclass__status=1,
            fk_subject=subject,
            fk_class=class_id,
            fk_term=term,
            date_presence=chosen_date

        ).annotate(
            student_name=F('fk_student_user__username'),
            registration=F('fk_student_user__registration'),
        ).values(
            'pk_student_presence',
            'fk_student_user',
            'student_name',
            'registration',
            'presence'
        )

        return list(query_result)

    def build_student_presence_data(self, user_id: int, 
                                   class_id: int, 
                                   term_id: int, 
                                   subject_id: int,
                                   chosen_date:str):
        """
        Constrói dados de faltas do aluno para criação.

        Args:
            user_id (int): O ID do usuário do aluno.
            class_id (int): O ID da turma associada à nota.
            term_id (int): O ID do período associado à nota.
            subject_id (int): O ID da disciplina associada à nota.

        Returns:
            tuple: Uma dict.
        """
        return {
            "fk_class": class_id,
            "fk_term": term_id,
            "fk_subject": subject_id,
            "fk_student_user": user_id,
            "date_presence":chosen_date
        }

    def create_student_presence(self, grade: dict):

        serializer = StudentPresenceCreateSerializer(data=grade)
        if serializer.is_valid():
            serializer.save()
            saved_data = serializer.data

            # removedo os item que não serão nescessário na listagem das notas
            items_to_remove = ('fk_class', 'fk_term', 'fk_subject', 'date_presence')

            for item in items_to_remove:
                saved_data.pop(item, None)

            return saved_data, None

        else:
            return (None, ResponseHelper.HTTP_400({'detail': serializer.errors}))
