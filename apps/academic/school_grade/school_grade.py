#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.academic.models import SchoolGrade
from apps.academic.school_grade.serializer import SchoolGradeSerializer


logger = logging.getLogger('django')


class BaseSchoolGrade():

    def get_object(self, pk) -> tuple:
        try:
            return (SchoolGrade.objects.get(pk=pk), None)
        except SchoolGrade.DoesNotExist:
            message = 'Não foi possivel encontrar este SchoolGrade.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (SchoolGrade.objects.all(), None)
        except SchoolGrade.DoesNotExist:
            message = 'Não foi possivel encontrar todos os SchoolGrade.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_school_grade_data(self, pk) -> tuple:
        """
            Captura os id da school_grade e dados serializados de um school_grade especifica
        """
        logger.info(f'Capturando dados do school_grade id:{pk}')
        school_grade_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = SchoolGradeSerializer(school_grade_id)
        return school_grade_id, selrializer.data
