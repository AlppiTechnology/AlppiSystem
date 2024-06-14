#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging

from datetime import datetime
from django.db.models import Q, F
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import HasPermission, IsViewAllowed
from alppi.responses import ResponseHelper
from alppi.utils.decorators import permission_required
from alppi.utils.groups import SUPERUSER
from apps.academic.models import PedagogicalSetting
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListPedagogicalView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            year = request.GET.get('year',None)
            search_status = request.GET.get('status', None)
            search_class_name = request.GET.get('search',None)
            fk_school_grade = request.GET.get('school_grade',None)
            jwt_token = request.jwt_token
            user_group = jwt_token.get('group').lower()
            registration = jwt_token.get('registration')

            class_settings = PedagogicalSetting.objects.filter(
                ).annotate(
                    school_grade_name=F('fk_class_setting__fk_school_grade__name'),
                    school_year_name=F('fk_class_setting__fk_school_year__year'),
                    school_level_name=F('fk_class_setting__fk_school_grade__fk_school_level__name'),
                    subject_name = F('fk_subject__subject_name'),
                    pk_class_setting = F('fk_class_setting'),
                    name = F('fk_class_setting__name')
                ).values('pk_pedagogical_setting','pk_class_setting','name',
                         'school_grade_name','school_level_name',
                         'school_year_name','status','subject_name'
                ).order_by('name','school_grade_name')

            # Filtra por ano letivo
            if year:
                class_settings = class_settings.filter(fk_school_year = year)

            # filtra pelo status 
            if search_status:
                class_settings = class_settings.filter(status = search_status)

            # filtra pelo nome da turma
            if search_class_name:
                class_settings = class_settings.filter(name = search_class_name)

            # filtra pela serie
            if fk_school_grade:
                class_settings = class_settings.filter(fk_school_grade = fk_school_grade)

            # busca somente pelas turma do Colaborador
            if user_group in ('avaliador','professor'):
                class_settings = class_settings.filter(fk_employee_user__registration = registration)

            class_setting_paginate = self.paginate_queryset(
                class_settings, request, view=self)


            return  ResponseHelper.HTTP_200(self.get_paginated_response(class_setting_paginate).data)


        except Exception as error:
            message = 'Problemas ao listar todos os ClassSetting.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})