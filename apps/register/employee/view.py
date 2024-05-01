#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging

from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import HasPermission, IsViewAllowed
from alppi.responses import ResponseHelper
from alppi.utils.decorators import load_system_modules, permission_required
from alppi.utils.groups import ADMINISTRATOR, SUPERUSER
from apps.register.models import User
from apps.register.employee.employee import BaseEmployee
from apps.register.employee.serializer import EmployeeSerializer
from common.util import uppercase_first
from common.cpf_cnpj.cpf_cnpj_validator import validate_cpf_cnpj
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class EmployeeView(APIView, BaseEmployee):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            user_obj, error = self.get_object(pk)
            if error:
                return error

            user_groups = [group.name.title()
                           for group in user_obj.groups.all()]

            serializer = EmployeeSerializer(user_obj)
            data = serializer.data
            data['user_groups'] = user_groups
            del (data['password'])
            return  ResponseHelper.HTTP_200({'results': data})

        except Exception as error:
            message = 'Problemas ao visualizar Usuario'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class UpdateEmployeeView(APIView, BaseEmployee):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:

        try:
            data = request.data

            if not ALPPIDEVEL and data.get('cpf') and not validate_cpf_cnpj(int(data.get('cpf'))):
                return  ResponseHelper.HTTP_400({'results': 'CNPJ-CPF invalido'})

            data['cpf'] = ''.join(filter(str.isdigit, data.get('cpf')))
            data['edited'] = datetime.now()

            # deixa as primeiras letras dos no
            uppercase_first(data, ['username'])

            user_obj, user_data = self.get_user_data(pk)
            if not user_obj:
                # Caso ocora algum erro, é retornado nesse return
                return user_data

            # dados que não são alterado ao editar dados dos usuarios
            data['registration'] = user_data['registration']
            data['password'] = user_data['password']
            data['fk_campus'] = user_data['fk_campus']
            data['last_login'] = user_data['last_login']
            updated_groups = set(data.get('groups'))

            serializer = EmployeeSerializer(user_obj, data=data)
            if serializer.is_valid():

                user_groups = (group.name for group in user_obj.groups.all())
                groups_del = (
                    group for group in user_groups if group not in updated_groups)
                groups_add = (
                    group for group in updated_groups if group not in user_groups)

                if groups_del:
                    # deletando os grupos do usuario
                    for group_name in groups_del:
                        group = Group.objects.get(name=group_name)

                        user_obj.groups.remove(group)

                if groups_add:
                    # adicionando os grupos ao usuario
                    for group_name in groups_add:
                        group = Group.objects.get(name=group_name)

                        user_obj.groups.add(group)

                serializer.save()

                data_salved = serializer.data
                data_salved['groups'] = updated_groups

                del (data_salved['password'])
                return  ResponseHelper.HTTP_200({'results': data_salved})

            return  ResponseHelper.HTTP_400({'results': serializer.error})

        except Exception as error:

            message = 'Problemas ao editar usuario'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteEmployeeView(APIView, BaseEmployee):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            user_obj, user_data = self.get_user_data(pk)
            if not user_obj:
                # Caso ocora algum erro, é retornado nesse return
                return user_data

            user_obj.delete()
            message = 'Usuario deletado com sucesso'
            logger.info({'results': message})
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:
            message = 'Problemas ao deletar Usuario'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ListEmployeeView(APIView, CustomPagination, BaseEmployee):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            logger.info('listando todas os Usuario cadastrados')
            search = request.GET.get('search', '')
            search_status = request.GET.get('status', '1')

            user_info = User.objects.filter(
                Q(username__icontains=search) |
                Q(registration__contains=search)
            ).exclude(
                groups__name='estudante'
            ).values('pk_user', 'registration', 'username', 'is_active')

            if search_status:
                user_info = user_info.filter(is_active=search_status)

            user_info = user_info.order_by(
                '-is_active', 'username', 'registration')
            user_paginate = self.paginate_queryset(
                user_info, request, view=self)

            return  ResponseHelper.HTTP_200({'results': self.get_paginated_response(user_paginate).data})


        except Exception as error:
            message = 'Problemas ao listar todos os Usuarios.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class CreateEmployeeView(APIView, BaseEmployee):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    @method_decorator(load_system_modules, name='dispatch')
    def post(self, request, format=None) -> ResponseHelper:

        try:
            data = request.data

            if not ALPPIDEVEL and data.get('cpf') and not validate_cpf_cnpj(int(data.get('cpf'))):
                return  ResponseHelper.HTTP_400({'results': 'CNPJ-CPF invalido'})

            data['cpf'] = ''.join(filter(str.isdigit, data.get('cpf')))
            data['edited'] = datetime.now()
            data['last_login'] = datetime.now()
            data['is_active'] = 1

            # deixa as primeiras letras dos no
            uppercase_first(data, ['username'])

            if not data.get('registration'):
                data['registration'] = self.get_last_registration()
            else:
                has_registreded = self.check_registration(
                    data.get('registration'))
                if has_registreded:
                    return has_registreded

            # Criptografa as senhas
            encrypted_pass = make_password(data.get('password'))
            data['password'] = encrypted_pass
            groups = set(data.get('groups'))

            serializer = EmployeeSerializer(data=data)
            if serializer.is_valid():

                serializer.save()
                data_salved = serializer.data

                user_obj, error = self.get_object(data_salved.get('pk_user'))
                if error:
                    return error
                # adicionando os grupos ao usuario
                for group_name in groups:
                    group = Group.objects.get(name=group_name)

                    user_obj.groups.add(group)

                data_salved['groups'] = groups
                del (data_salved['password'])
                return  ResponseHelper.HTTP_201({'results': data_salved})

            return  ResponseHelper.HTTP_400({'results': serializer.errors})

        except Exception as error:
            if user_obj:
                user_obj.delete()

            message = 'Problemas ao criar usuario'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ChangeStatusEmployeeView(APIView, BaseEmployee):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    @method_decorator(load_system_modules, name='dispatch')
    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            user_obj, user_data = self.get_user_data(pk)
            if not user_obj:
                # Caso ocora algum erro, é retornado nesse return
                return user_data

            user_obj.is_active = data.get('is_active')
            user_obj.edited = datetime.now()
            user_obj.save()
            logger.info('Alterando status do usuario para {}.'.format(
                data.get('is_active')))

            message = 'Usuário atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status de usuario'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})
