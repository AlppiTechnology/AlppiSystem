#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.academic.models import SchoolYear
from apps.academic.school_year.serializer import SchoolYearSerializer


logger = logging.getLogger('django')


class BaseSchoolYear():

    def get_object(self, pk) -> tuple:
        try:
            return (SchoolYear.objects.get(pk=pk), None)
        except SchoolYear.DoesNotExist:
            message = 'Não foi possivel encontrar este SchoolYear.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (SchoolYear.objects.all(), None)
        except SchoolYear.DoesNotExist:
            message = 'Não foi possivel encontrar todos os SchoolYear.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_school_year_data(self, pk) -> tuple:
        """
            Captura os id da school_year e dados serializados de um school_year especifica
        """
        logger.info(f'Capturando dados do school_year id:{pk}')
        school_year_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = SchoolYearSerializer(school_year_id)
        return school_year_id, selrializer.data
    
    def delete_school_year(self, pk):
        """
        Deleta a school year especifico
        """
        school_year_obj, error = self.get_object(pk)
        if error:
            return error

        school_year_obj.delete()
