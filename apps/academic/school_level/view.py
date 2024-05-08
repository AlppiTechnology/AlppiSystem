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
from alppi.utils.groups import SUPERUSER, ADMINISTRATOR
from apps.academic.school_level.school_level import BaseSchoolLevel
from apps.academic.school_level.serializer import SchoolLevelSerializer
from apps.academic.models import SchoolLevel
from common.pagination.pagination import CustomPagination
from common.util import uppercase_first


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class SchoolLevelView(APIView, BaseSchoolLevel):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            school_level_obj, error = self.get_object(pk)
            if error:
                return error
            
            serializer = SchoolLevelSerializer(school_level_obj)
            return  ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar SchoolLevel'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
        
@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ListSchoolLevelView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            school_level = SchoolLevel.objects.all()
            shift_paginate = self.paginate_queryset(
                school_level, request, view=self)

            serializer = SchoolLevelSerializer(
                shift_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)


        except Exception as error:
            message = 'Problemas ao listar todos os SchoolLevel.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class UpdateSchoolLevelView(APIView, BaseSchoolLevel):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            uppercase_first(data, ['name'])

            school_level_obj, error = self.get_object(pk)
            if error:
                return error

            serializer = SchoolLevelSerializer(school_level_obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar SchoolLevel'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class CreateSchoolLevelView(APIView):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data
            uppercase_first(data, ['name'])

            serializer = SchoolLevelSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_201({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar SchoolLevel'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteSchoolLevelView(APIView, BaseSchoolLevel):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            school_level_obj, error = self.get_object(pk)
            if error:
                return error
            
            school_level_obj.delete()
            return  ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar SchoolLevel'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})