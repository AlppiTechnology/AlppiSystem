#!/usr/bin/python
# -*- encoding: utf-8 -*-
from datetime import datetime
import logging
from django.db.models import Q, F

from alppi.responses import ResponseHelper
from apps.academic.models import SkillGrade
from apps.academic.skill_grade.serializer import SkillGradeCreateSerializer, SkillGradeSerializer


logger = logging.getLogger('django')


class BaseSkillGrade():

    def get_object(self, pk) -> tuple:
        try:
            return (SkillGrade.objects.get(pk=pk), None)
        except SkillGrade.DoesNotExist:
            message = 'Não foi possivel encontrar este SkillGrade.'
            logger.error({'results': message})
            return (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (SkillGrade.objects.all(), None)
        except SkillGrade.DoesNotExist:
            message = 'Não foi possivel encontrar todos os SkillGrade.'
            logger.error({'results': message})
            return (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_skill_grade_data(self, pk) -> tuple:
        """
            Captura os id da skill_grade e dados serializados de um skill_grade especifica
        """
        logger.info(f'Capturando dados do skill_grade id:{pk}')
        skill_grade_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = SkillGradeSerializer(skill_grade_id)
        return skill_grade_id, selrializer.data

    def get_students_skill_grade(self, subject: int, skill_id:int, 
                                 class_id: int, term: int):

        query_result = SkillGrade.objects.filter(
            fk_student_user__studentclass__status=1,
            fk_subject=subject,
            fk_skill=skill_id,
            fk_class=class_id,
            fk_term=term

        ).annotate(
            student_name=F('fk_student_user__username'),
            registration=F('fk_student_user__registration'),
        ).values(
            'pk_skill_grade',
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

    def build_student_skill_grade_data(self, user_id:int, class_id:int, 
                                 term_id:int, subject_id:int, skill_id:int):
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
            "fk_skill":skill_id,
            "fk_student_user": user_id
        }

    def create_student_skill_grade(self, skill_grade: dict):
        skill_grade['edited'] = datetime.now()
        skill_grade['status'] = 1

        serializer = SkillGradeCreateSerializer(data=skill_grade)
        if serializer.is_valid():
            serializer.save()
            saved_data = serializer.data

            # removedo os item que não serão nescessário na listagem das notas
            items_to_remove = ('fk_class', 'fk_term', 'fk_subject',
                               'edited', 'status', 'fk_skill')
            
            for item in items_to_remove:
                saved_data.pop(item, None)

            return saved_data, None

        else:
            return (None, ResponseHelper.HTTP_400({'detail': serializer.errors}))
