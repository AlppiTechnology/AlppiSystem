#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import logging

from datetime import datetime
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from alppi.responses import ResponseHelper
from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import HasPermission, IsViewAllowed
from alppi.utils.decorators import permission_required
from alppi.utils.groups import ADMINISTRATOR, SUPERUSER
from apps.academic.subject_area.subject_area import BaseSubjectArea
from apps.academic.subject_area.serializer import SubjectAreaSerializer
from apps.academic.models import SubjectArea
from apps.academic.subject_area.validations import validate_subject_area_name

from common.pagination.pagination import CustomPagination
from common.util import uppercase_first


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class SubjectAreaView(APIView, BaseSubjectArea):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            subject_area_obj, error = self.get_object(pk)
            if error:
                return error

            serializer = SubjectAreaSerializer(subject_area_obj)
            return ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar SubjectArea'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ListSubjectAreaView(APIView, BaseSubjectArea, CustomPagination):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None)-> ResponseHelper:
        try:
            search_area = request.GET.get('search', None)
            search_status = request.GET.get('status', '1')

            fk_campus = request.jwt_token.get('pk_campus')

            subject_area = SubjectArea.objects.filter(fk_campus=fk_campus
                                                      ).values('pk_subject_area', 'name', 'status')

            # filtra deacordo com a area pessada por parametro
            if search_area:
                subject_area = subject_area.filter(name__icontains=search_area)

            # filtra de acordo com o status passado por parametro
            if search_status:
                subject_area = subject_area.filter(status=search_status)

            # Ordenando por status e nome
            subject_area = subject_area.order_by('-status', 'name')

            subject_area_paginate = self.paginate_queryset(
                subject_area, request, view=self)

            return ResponseHelper.HTTP_200(self.get_paginated_response(subject_area_paginate).data)

        except Exception as error:
            message = 'Problemas ao visualizar SubjectArea'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class UpdateSubjectAreaView(APIView, BaseSubjectArea):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None)-> ResponseHelper:
        try:
            data = request.data

            subject_area_obj, subject_area_data = self.get_subject_area_data(
                pk)
            if not subject_area_obj:
                return subject_area_data

            assert validate_subject_area_name(data)

            subject_area_data['edited'] = datetime.now()
            subject_area_data['name'] = data.get('name')
            subject_area_data['status'] = 1 if data.get('status') else 0

            # deixa as primeiras letras dos nomes maiusculas
            uppercase_first(subject_area_data, ['name'])

            serializer = SubjectAreaSerializer(
                subject_area_obj, data=subject_area_data)
            if serializer.is_valid():
                serializer.save()
                return ResponseHelper.HTTP_200({'results': serializer.data})

            return ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar Subject Area'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteSubjectAreaView(APIView, BaseSubjectArea):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None)-> ResponseHelper:
        try:
            subject_area_obj, error = self.get_object(pk)
            if error:
                return error

            subject_area_obj.delete()
            return ResponseHelper.HTTP_204()


        except Exception as error:
            message = 'Problemas ao deletar SubjectArea'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class CreateSubjectAreaView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None)-> ResponseHelper:
        try:
            data = request.data

            assert validate_subject_area_name(data)

            data['fk_campus'] = request.jwt_token.get('pk_campus')
            data['edited'] = datetime.now()
            data['status'] = 1

            # deixa as primeiras letras dos nomes maiusculas
            uppercase_first(data, ['name'])

            serializer = SubjectAreaSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return ResponseHelper.HTTP_201({'results': serializer.data})

            return ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar Subject Area'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ChangeStatusSubjectAreaView(APIView, BaseSubjectArea):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            subject_area_obj, error = self.get_object(pk)
            if error:
                return error

            subject_area_obj.status = data.get('status')
            subject_area_obj.save()
            logger.info('Alterando status do subject_area para {}.'.format(
                data.get('is_active')))

            message = 'Area do conhecimento atualizado com sucesso.'
            return ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do subject_area'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
