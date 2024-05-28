#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging

from datetime import datetime
from django.utils.decorators import method_decorator
from django.db.models import Min, Max

from rest_framework.views import APIView

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import HasPermission, IsViewAllowed
from alppi.responses import ResponseHelper
from alppi.utils.decorators import permission_required
from alppi.utils.groups import SUPERUSER
from apps.academic.models import SchoolYear
from apps.academic.school_year.school_year import BaseSchoolYear
from apps.academic.school_year.serializer import SchoolYearSerializer
from apps.academic.school_year_date.school_year_date import BaseSchoolYearDate
from apps.academic.school_year_skill.school_year_skill import BaseSchoolYearSkill
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class SchoolYearView(APIView, BaseSchoolYear):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            school_year_obj, school_year_data = self.get_school_year_data(pk)
            if not school_year_obj:
                return school_year_data
            
            BSYD = BaseSchoolYearDate()
            dates, error = BSYD.list_school_year_date(school_year_data.get('pk_school_year'))
            if error:
                return error
            
            school_year_data['dates'] = dates

            if school_year_data.get('skill'):
                BSYS = BaseSchoolYearSkill()
                skill_list = BSYS.list_school_year_skill(school_year_data.get('pk_school_year'))

                school_year_data['skill_list'] = skill_list

            return ResponseHelper.HTTP_200({'results': school_year_data})

        except Exception as error:
            message = 'Problemas ao visualizar SchoolYear'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class UpdateSchoolYearView(APIView, BaseSchoolYear):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            dates = data.pop('dates')
            skill = data.get('skill')
            skills_list = data.pop('skill_list', [])

            BSYD = BaseSchoolYearDate()
            BSYS = BaseSchoolYearSkill()

            school_year_obj, school_year_data = self.get_school_year_data(pk)
            if not school_year_obj:
                return school_year_data
            
            data['fk_term_type'] = school_year_data.get('fk_term_type')
            data['fk_campus'] = school_year_data.get('fk_campus')
            data['edited'] = datetime.now()


            _, error = BSYD.update_school_year_date(data=data, dates=dates)
            if error:
                return error


            serializer = SchoolYearSerializer(school_year_obj, data=data)
            if serializer.is_valid():
                # serializer.save()

                if skill:
                    _, has_error = BSYS.update_school_year_skill(skills_list, pk)
                    if has_error:
                        return has_error
                    
                return ResponseHelper.HTTP_200({'results': serializer.data})

            return ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar SchoolYear'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteSchoolYearView(APIView, BaseSchoolYear):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            BSYD = BaseSchoolYearDate()
            BSYS = BaseSchoolYearSkill()

            school_year_obj, error = self.get_object(pk)
            if error:
                return error
            
            # _, error = BSYD.delete_school_year_date(pk)
            # if error:
            #     return error
            
            # _, error = BSYS.delete_school_year_skill(pk)
            # if error:
            #     return error


            school_year_obj.delete()
            return ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar SchoolYear'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListSchoolYearView(APIView, CustomPagination):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            school_year = SchoolYear.objects.annotate(
                menor_data_init=Min('schoolyeardate__init_date'),
                maior_data_final=Max('schoolyeardate__final_date')
            ).values(
                'pk_school_year', 'year', 'total_grade', 'average_grade', 
                'status', 'menor_data_init', 'maior_data_final'
            )
            school_year_paginate = self.paginate_queryset(
                school_year, request, view=self)

            return ResponseHelper.HTTP_200(self.get_paginated_response(school_year_paginate).data)

        except Exception as error:
            message = 'Problemas ao listar todos os SchoolYear.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CreateSchoolYearView(APIView, BaseSchoolYear):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data

            data['fk_campus'] = request.jwt_token.get('pk_campus')
            data['edited'] = datetime.now()
            data['status'] = 1
            dates = data.get('dates')
            skill = data.get('skill')
            skills_list = data.get('skill_list', [])

            serializer = SchoolYearSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                saved_data = serializer.data

                BSYD = BaseSchoolYearDate()
                school_year_date_ids, error = BSYD.create_school_year_date(
                    saved_data, dates)
                if error:
                    self.delete_school_year(saved_data.get('pk_school_year'))
                    return error

                if skill:
                    BSYS = BaseSchoolYearSkill()
                    _, error = BSYS.create_school_year_skill(
                        skills_list, saved_data.get('pk_school_year'))
                    if error:
                        BSYD.delete_school_year_date(school_year_date_ids)
                        self.delete_school_year(
                            saved_data.get('pk_school_year'))
                        return error

                return ResponseHelper.HTTP_201({'results': saved_data})

            return ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYear'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ChangeStatusSchoolYearView(APIView, BaseSchoolYear):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            school_year_obj, error = self.get_object(pk)
            if error:
                return error

            school_year_obj.status = data.get('status')
            school_year_obj.save()
            logger.info('Alterando status do school_year para {}.'.format(
                data.get('status')))

            message = 'SchoolYear atualizado com sucesso.'
            return ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do school_year'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
