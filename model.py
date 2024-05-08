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
from alppi.utils.groups import SUPERUSER
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class Troca1View(APIView, BaseTroca1):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            troca2_obj, error = self.get_object(pk)
            if error:
                return error
            
            serializer = Troca1Serializer(troca2_obj)
            return  ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar Troca1'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class UpdateTroca1View(APIView, BaseTroca1):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data

            troca2_obj, error = self.get_object(pk)
            if error:
                return error

            serializer = Troca1Serializer(troca2_obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar Troca1'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListTroca1View(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            troca2s = Troca1.objects.all()
            troca2_paginate = self.paginate_queryset(
                troca2s, request, view=self)

            serializer = Troca1Serializer(
                troca2_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)


        except Exception as error:
            message = 'Problemas ao listar todos os Troca1.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CreateTroca1View(APIView):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data

            serializer = Troca1Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_201({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar Troca1'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteTroca1View(APIView, BaseTroca1):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            troca2_obj, error = self.get_object(pk)
            if error:
                return error
            
            troca2_obj.delete()
            return  ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar Troca1'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ChangeStatusTroca1View(APIView, BaseTroca1):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]
    
    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            troca2_obj, error = self.get_object(pk)
            if error:
                return error

            troca2_obj.is_active = data.get('is_active')
            troca2_obj.save()
            logger.info('Alterando status do troca2 para {}.'.format(data.get('is_active')))

            message = 'Troca1 atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do troca2'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})