#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging

from datetime import datetime
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import HasPermission,  IsViewAllowed
from alppi.responses import ResponseHelper
from alppi.utils.decorators import permission_required
from alppi.utils.groups import SUPERUSER
from apps.register.campus.campus import BaseCampus
from apps.register.campus.serializer import CampusSerializer

from common.cpf_cnpj.cpf_cnpj_validator import validate_cpf_cnpj
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CampusView(APIView, BaseCampus):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None, *args, **kwargs) -> ResponseHelper:

        try:
            campus_obj, error = self.get_object(pk)
            if error:
                return error

            serializer = CampusSerializer(campus_obj)
            return  ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar Campus'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class UpdateCampusView(APIView, BaseCampus):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:

        try:
            data = request.data

            campus_obj, campus_data = self.get_campus_data(pk)
            if not campus_obj:
                return campus_data

            if not ALPPIDEVEL and data.get('cnpj') and not validate_cpf_cnpj(data.get('cnpj')):
                return  ResponseHelper.HTTP_400({'results': 'CNPJ-CPF invalido'})

            data['cnpj'] = ''.join(filter(str.isdigit, data.get('cnpj')))
            data['edited'] = datetime.now()
            data['campus_code'] = campus_data.get('campus_code')

            serializer = CampusSerializer(campus_obj, data=data)
            if serializer and serializer.is_valid():

                serializer.save()
                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'results': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar Campus'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteCampusView(APIView, BaseCampus):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            campus_obj, campus_data = self.get_campus_data(pk)
            if not campus_obj:
                return campus_data
            
            campus_obj.delete()
            message = 'Campus deletado com sucesso'
            logger.info({'results': message})
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:
            message = 'Problemas ao deletar Campus'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListCampusView(APIView, CustomPagination, BaseCampus):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            campus, error = self.get_all_object()
            if error:
                return error

            campus_paginate = self.paginate_queryset(
                campus, request, view=self)

            serializer = CampusSerializer(
                campus_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)

        except Exception as error:
            message = 'Problemas ao listar todos os Campus.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CreateCampusView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:

        try:
            data = request.data

            if not ALPPIDEVEL and data.get('cnpj') and not validate_cpf_cnpj(data.get('cnpj')):
                return  ResponseHelper.HTTP_400({'results': 'CNPJ-CPF invalido'})

            data['cnpj'] = ''.join(filter(str.isdigit, data.get('cnpj')))
            data['edited'] = datetime.now()
            data['status'] = 1

            serializer = CampusSerializer(data=data)
            if serializer.is_valid():

                serializer.save()
                return  ResponseHelper.HTTP_201({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'results': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar Campus'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ChangeStatusCampusView(APIView, BaseCampus):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            campus_obj, error = self.get_object(pk)
            if error:
                return error

            campus_obj.is_active = data.get('is_active')
            campus_obj.save()
            logger.info('Alterando status do campus para {}.'.format(
                data.get('is_active')))

            message = 'Usuário atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do campus'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})
