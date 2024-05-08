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
from apps.academic.term_type.serializer import TermTypeSerializer
from apps.academic.models import TermType
from apps.academic.term_type.term_type import BaseTermType
from common.pagination.pagination import CustomPagination
from common.util import uppercase_first


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ListTermTypeView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            term_types = TermType.objects.all()
            term_type_paginate = self.paginate_queryset(
                term_types, request, view=self)

            serializer = TermTypeSerializer(
                term_type_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)


        except Exception as error:
            message = 'Problemas ao listar todos os TermType.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class TermTypeView(APIView, BaseTermType):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            term_type_obj, error = self.get_object(pk)
            if error:
                return error
            
            serializer = TermTypeSerializer(term_type_obj)
            return  ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar TermType'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class CreateTermTypeView(APIView):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data
            uppercase_first(data, ['name'])

            serializer = TermTypeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_201({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar TermType'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class UpdateTermTypeView(APIView, BaseTermType):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            uppercase_first(data, ['name'])

            term_type_obj, error = self.get_object(pk)
            if error:
                return error

            serializer = TermTypeSerializer(term_type_obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar TermType'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteTermTypeView(APIView, BaseTermType):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            term_type_obj, error = self.get_object(pk)
            if error:
                return error
            
            term_type_obj.delete()
            return  ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar TermType'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
