#!/usr/bin/python
# -*- encoding: utf-8 -*-
from datetime import datetime
import logging
from django.db.models import Q, F

from alppi.responses import ResponseHelper
from apps.academic.models import SubjectGrade
from apps.academic.subject_grade.serializer import SubjectGradeCreateSerializer, SubjectGradeSerializer


logger = logging.getLogger('django')


class BaseSubjectGrade():

    def get_object(self, pk) -> tuple:
        try:
            return (SubjectGrade.objects.get(pk=pk), None)
        except SubjectGrade.DoesNotExist:
            message = 'Não foi possivel encontrar este SubjectGrade.'
            logger.error({'results': message})
            return (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (SubjectGrade.objects.all(), None)
        except SubjectGrade.DoesNotExist:
            message = 'Não foi possivel encontrar todos os SubjectGrade.'
            logger.error({'results': message})
            return (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_subject_grade_data(self, pk) -> tuple:
        """
            Captura os id da subject_grade e dados serializados de um subject_grade especifica
        """
        logger.info(f'Capturando dados do subject_grade id:{pk}')
        subject_grade_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = SubjectGradeSerializer(subject_grade_id)
        return subject_grade_id, selrializer.data

    def get_students_grade(self, subject: int, class_id: int, term: int):

        query_result = SubjectGrade.objects.filter(
            fk_student_user__studentclass__status=1,
            fk_subject=subject,
            fk_class=class_id,
            fk_term=term

        ).annotate(
            student_name=F('fk_student_user__username'),
            registration=F('fk_student_user__registration'),
        ).values(
            'pk_subject_grade',
            'fk_student_user',
            'student_name',
            'registration',
            'grade_1',
            'grade_2',
            'grade_3',
            'grade_4',
            'grade_5'
        )

        return list(query_result)

    def build_student_grade_data(self, user_id, class_id, term_id, subject_id):
        """
        Constrói dados de notas do aluno para criação.

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
            "fk_student_user": user_id
        }

    def create_student_grade(self, grade: dict):
        grade['edited'] = datetime.now()
        grade['status'] = 1

        serializer = SubjectGradeCreateSerializer(data=grade)
        if serializer.is_valid():
            serializer.save()
            saved_data = serializer.data

            # removedo os item que não serão nescessário na listagem das notas
            items_to_remove = ('fk_class', 'fk_term', 'fk_subject',
                               'edited', 'status')
            
            for item in items_to_remove:
                saved_data.pop(item, None)

            return saved_data, None

        else:
            return (None, ResponseHelper.HTTP_400({'detail': serializer.errors}))
