#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from django.db.models import Q, F

from alppi.responses import ResponseHelper
from apps.academic.models import SchoolYearDate
from apps.academic.school_year_date.serializer import SchoolYearDateSerializer
from apps.academic.school_year_date.validations import validate_dates, validate_term_grade, validate_terms


TERM_TYPE_1 = (1, 2, 3, 4)
TERM_TYPE_2 = (5, 6, 7)
TERM_TYPE_3 = (8, 9)

logger = logging.getLogger('django')


class BaseSchoolYearDate():

    def get_object(self, pk) -> tuple:
        try:
            return (SchoolYearDate.objects.get(pk=pk), None)
        except SchoolYearDate.DoesNotExist:
            message = 'Não foi possivel encontrar este SchoolYearDate.'
            logger.error({'results': message})
            return (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (SchoolYearDate.objects.all(), None)
        except SchoolYearDate.DoesNotExist:
            message = 'Não foi possivel encontrar todos os SchoolYearDate.'
            logger.error({'results': message})
            return (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_school_year_date_data(self, pk) -> tuple:
        """
            Captura os id da school_year_date e dados serializados de um school_year_date especifica
        """
        logger.info(f'Capturando dados do school_year_date id:{pk}')
        school_year_date_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = SchoolYearDateSerializer(school_year_date_id)
        return school_year_date_id, selrializer.data

    def list_school_year_date(self, fk_school_year: int):

        try:
            school_year_date_data = SchoolYearDate.objects.annotate(
                term_name=F('fk_term__name')
            ).filter(
                fk_school_year=fk_school_year
            ).values('pk_school_year_date', 'grade', 'init_date', 
                     'final_date', 'term_name', 'fk_term'
                     ).order_by('term_name')

            if school_year_date_data:
                return list(school_year_date_data), None

            return [], None

        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def list_pk_school_year_date(self ,fk_school_year: int):
        try:
            pk_school_year_date = SchoolYearDate.objects.filter(
                fk_school_year=fk_school_year
            ).values('pk_school_year_date')

            if pk_school_year_date:
                return list(pk_school_year_date)

            return []

        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def create_school_year_date(self, data: dict, dates: dict):

        try:
            pk_school_year = data.get('pk_school_year')
            term_type = data.get('fk_term_type')
            total_grade = data.get('total_grade')

            error = validate_terms(dates, term_type)
            if error:
                return None, error
            error = validate_dates(dates)
            if error:
                return None, error
            error = validate_term_grade(dates, total_grade)
            if error:
                return None, error

            # saved_school_year_date = []
            school_year_date_id = []

            for date in dates:
                date['fk_school_year'] = pk_school_year

                serializer = SchoolYearDateSerializer(data=date)
                if serializer.is_valid():
                    serializer.save()

                    saved_data = serializer.data

                    school_year_date_id.append(
                        saved_data.get('pk_school_year_date'))
                    # saved_school_year_date.append(saved_data)

                else:
                    return None, ResponseHelper.HTTP_400({'detail': serializer.errors})

            return school_year_date_id, None

        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def delete_school_year_date(self, fk_school_year:int):
        try:
            school_year_date_obj = SchoolYearDate.objects.filter(
                fk_school_year=fk_school_year)

            school_year_date_obj.delete()

            return None, None
        
        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def update_school_year_date(self, data: dict, dates: dict):
        try:
            # term_type = data.get('fk_term_type')
            total_grade = data.get('total_grade')

            # error = validate_terms(dates, term_type)
            # if error:
            #     return None, error
            error = validate_dates(dates)
            if error:
                return None, error
            error = validate_term_grade(dates, total_grade)
            if error:
                return None, error

            for index_date in dates:
                school_year_date_obj, error = self.get_object(index_date.get('pk_school_year_date'))
                if error:
                    return None, error
                
                index_date['fk_term'] = school_year_date_obj.fk_term_id
                index_date['fk_school_year'] = school_year_date_obj.fk_school_year_id
                
                serializer = SchoolYearDateSerializer(school_year_date_obj, data=index_date)
                if serializer.is_valid():
                    serializer.save()


                else:
                    return None, ResponseHelper.HTTP_400({'detail': serializer.errors})
            
            return None, None

        except Exception as error:
            message = 'Problemas ao Atualizar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def get_school_year_date_info(self, fk_school_year: int, term: int):
        try:
            school_year_date_data = SchoolYearDate.objects.annotate(
                term_name=F('fk_term__name'),
                skill=F('fk_school_year__skill'),
                total_grade=F('fk_school_year__total_grade'),
                average_grade=F('fk_school_year__average_grade')
            ).filter(
                fk_school_year=fk_school_year,
                fk_term=term
            ).values('pk_school_year_date', 'grade', 'init_date', 
                     'final_date', 'term_name',
                     'total_grade', 'average_grade', 'skill'
            ).order_by('term_name').first()

            if school_year_date_data:
                return school_year_date_data, None

            message = 'Esse termo não pertece ao ano letivo'
            return None, ResponseHelper.HTTP_400({'detail': message})

        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})