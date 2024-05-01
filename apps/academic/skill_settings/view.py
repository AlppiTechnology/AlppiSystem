#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import logging

from datetime import datetime
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import HasPermission, IsViewAllowed
from alppi.responses import ResponseHelper
from alppi.utils.decorators import permission_required
from alppi.utils.groups import ADMINISTRATOR, SUPERUSER
from apps.academic.skill_settings.serializer import SkillSettingsSerializer
from apps.academic.models import SkillSettings
from apps.academic.skill_settings.skill_settings import BaseSkillSettings
from apps.academic.skill_settings.validations import validate_description, validate_label_name

from common.pagination.pagination import CustomPagination
from common.util import uppercase_first



logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class SkillSettingsView(APIView, BaseSkillSettings):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            skill_settings_obj, error = self.get_object(pk)
            if error:
                return error
            
            serializer = SkillSettingsSerializer(skill_settings_obj)
            return ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar SkillSettings'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ListSkillSettingsView(APIView, BaseSkillSettings, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:

        try:
            label_name = request.GET.get('label_name', None)
            search_status = request.GET.get('status', '1')
            
            fk_campus = request.jwt_token.get('pk_campus')

            skill_settings = SkillSettings.objects.filter(fk_campus=fk_campus
                                ).values('pk_skill_setting','label_name', 'description', 'status')

            # filtra deacordo com a skill_settings pessada por parametro
            if label_name:
                skill_settings = skill_settings.filter(label_name__icontains=label_name)

            # filtra de acordo com o status passado por parametro
            if search_status:
                skill_settings = skill_settings.filter(status=search_status)

            # Ordenando por status e nome
            skill_settings = skill_settings.order_by('-status', 'label_name')

            skill_settings_paginate = self.paginate_queryset(skill_settings, request, view=self)

            return ResponseHelper.HTTP_200(self.get_paginated_response(skill_settings_paginate).data)


        except Exception as error:
            message = 'Problemas ao visualizar SkillSettings'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class UpdateSkillSettingsView(APIView, BaseSkillSettings):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data

            skill_settings_obj, skill_settings_data = self.get_skill_settings_data(pk)
            if not skill_settings_obj:
                return skill_settings_data
            
            assert validate_label_name(data)
            assert validate_description(data)


            skill_settings_data['edited'] = datetime.now()
            skill_settings_data['label_name'] = data.get('label_name')
            skill_settings_data['description'] = data.get('description')
            skill_settings_data['status'] = 1 if data.get('status') else 0

            # deixa as primeiras letras dos nomes maiusculas
            uppercase_first(skill_settings_data, ['label_name'])

            serializer = SkillSettingsSerializer(skill_settings_obj, data=skill_settings_data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar SkillSettings Area'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteSkillSettingsView(APIView, BaseSkillSettings):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            skill_settings_obj, error = self.get_object(pk)
            if error:
                return error
            
            skill_settings_obj.delete()
            return  ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar SkillSettings'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class CreateSkillSettingsView(APIView):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data

            assert validate_label_name(data)
            assert validate_description(data)

            data['fk_campus'] = request.jwt_token.get('pk_campus')
            data['status'] = 1

            # deixa as primeiras letras dos nomes maiusculas
            uppercase_first(data, ['label_name'])

           
            serializer = SkillSettingsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f'Disciplina cadastrada com sucesso')
                return  ResponseHelper.HTTP_201({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar SkillSettings Area'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ChangeStatusSkillSettingsView(APIView, BaseSkillSettings):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]
    
    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            skill_settings_obj, error = self.get_object(pk)
            if error:
                return error

            skill_settings_obj.status = data.get('status')
            skill_settings_obj.save()
            logger.info('Alterando status do skill_settings para {}.'.format(data.get('is_active')))

            message = 'Habilidade atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do skill_settings'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})