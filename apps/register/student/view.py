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
from apps.register.student.student import BaseStudent
from apps.register.student.serializer import StudentSerializer
from common.util import uppercase_first
from common.cpf_cnpj.cpf_cnpj_validator import validate_cpf_cnpj
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class StudentView(APIView, BaseStudent):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            student_obj, error = self.get_object(pk)
            if error:
                return error
            
            group_names = [group.name for group in student_obj.groups.all()]
            if 'estudante' not in group_names:
                message = 'Este usuario não é Estudante'
                return ResponseHelper.HTTP_400({'results': message})

            serializer = StudentSerializer(student_obj)
            data = serializer.data
            data.pop('password')
            data.pop('is_superuser')
            data.pop('is_staff')

            return  ResponseHelper.HTTP_200({'results': data})

        except Exception as error:
            message = 'Problemas ao visualizar Estudante'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class UpdateStudentView(APIView, BaseStudent):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:

        try:
            data = request.data

            if not ALPPIDEVEL and data.get('cpf') and not validate_cpf_cnpj(int(data.get('cpf'))):
                return  ResponseHelper.HTTP_400({'results': 'CNPJ-CPF invalido'})

            data['cpf'] = ''.join(filter(str.isdigit, data.get('cpf')))
            data['edited'] = datetime.now()
            data['is_superuser'] = False
            data['is_staff'] = False

            # deixa as primeiras letras dos no
            uppercase_first(data, ['username'])

            student_obj, student_data = self.get_student_data(pk)
            if not student_obj:
                # Caso ocora algum erro, é retornado nesse return
                return student_data

            # dados que não são alterado ao editar dados dos usuarios
            data['registration'] = student_data['registration']
            data['password'] = student_data['password']
            data['fk_campus'] = student_data['fk_campus']
            data['last_login'] = student_data['last_login']

            serializer = StudentSerializer(student_obj, data=data)
            if serializer.is_valid():

                serializer.save()

                data_salved = serializer.data
                data_salved['groups'] = ['estudante']

                data_salved.pop('password')
                data_salved.pop('is_superuser')
                data_salved.pop('is_staff')
                return  ResponseHelper.HTTP_200({'results': data_salved})

            return  ResponseHelper.HTTP_400({'results': serializer.error})

        except Exception as error:

            message = 'Problemas ao editar usuario'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteStudentView(APIView, BaseStudent):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            student_obj, student_data = self.get_student_data(pk)
            if not student_obj:
                # Caso ocora algum erro, é retornado nesse return
                return student_data

            student_obj.delete()
            message = 'Estudante deletado com sucesso'
            logger.info({'results': message})
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:
            message = 'Problemas ao deletar Estudante'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ListStudentView(APIView, CustomPagination, BaseStudent):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            logger.info('listando todas os Estudante cadastrados')
            search = request.GET.get('search', '')
            search_status = request.GET.get('status', '1')

            student_info = User.objects.filter(
                Q(username__icontains=search) |
                Q(registration__contains=search),
                groups__name='estudante'
            ).values('pk_user', 'registration', 'username', 'is_active')

            if search_status:
                student_info = student_info.filter(is_active=search_status)

            student_info = student_info.order_by(
                '-is_active', 'username', 'registration')
            student_paginate = self.paginate_queryset(
                student_info, request, view=self)

            return  ResponseHelper.HTTP_200(self.get_paginated_response(student_paginate).data)


        except Exception as error:
            message = 'Problemas ao listar todos os Estudantes.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class CreateStudentView(APIView, BaseStudent):
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
            data['is_superuser'] = False
            data['is_staff'] = False

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

            serializer = StudentSerializer(data=data)
            if serializer.is_valid():

                serializer.save()
                data_salved = serializer.data

                student_obj, error = self.get_object(data_salved.get('pk_user'))
                if error:
                    return error
                
                # adicionando os grupos ao usuario
                group = Group.objects.get(name='estudante')

                student_obj.groups.add(group)

                data_salved['groups'] = ['estudante']
                data_salved.pop('password')
                data_salved.pop('is_superuser')
                data_salved.pop('is_staff')

                return  ResponseHelper.HTTP_201({'results': data_salved})

            return  ResponseHelper.HTTP_400({'results': serializer.errors})

        except Exception as error:
            if student_obj:
                student_obj.delete()

            message = 'Problemas ao criar usuario'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ChangeStatusStudentView(APIView, BaseStudent):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    @method_decorator(load_system_modules, name='dispatch')
    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            student_obj, student_data = self.get_student_data(pk)
            if not student_obj:
                # Caso ocora algum erro, é retornado nesse return
                return student_data

            student_obj.is_active = data.get('is_active')
            student_obj.edited = datetime.now()
            student_obj.save()
            logger.info('Alterando status do usuario para {}.'.format(
                data.get('is_active')))

            message = 'Usuário atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status de usuario'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})
