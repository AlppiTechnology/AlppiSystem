#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging

from datetime import datetime
from django.db.models import Q
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import IsAuthenticatedAlppi, IsViewAllowed
from alppi.utils.decorators import permission_model_required
from apps.register.user.user import BaseUser
from common.conn_microservices.ms3.permission_conn import PermissionConn
from common.conn_microservices.ms3.user_conn import BuilderUserData, UserConn

from common.cpf_cnpj.cpf_cnpj_validator import validate_cpf_cnpj
from common.pagination.pagination import CustomPagination

from django.contrib.auth.models import Group, Permission

logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

STAFF = (1, 4, 5)
EMPLOYEE = (1, 2, 3, 4, 5, 8, 9)
STUDENT = (1, 2, 3, 4, 5, 8, 9)


@method_decorator(permission_model_required('permission'), name='dispatch')
class PermissionView(APIView, BaseUser):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, IsAuthenticatedAlppi]

    def get(self, request, pk, format=None):

        try:
            user_obj, user_data = self.get_user_data(pk)
            if not user_obj:
                # Caso ocora algum erro, é retornado nesse return
                return user_data
            
            builder_data = BuilderUserData()
            builder_data.set_data(user_data)
            builder_data.build_params()
            params = builder_data.get_params()

            # captura informações do usuario ms3
            user_conn = UserConn(request.headers.get('Authorization'))
            response_ms3 = user_conn.filter_user_ms3(params)

            # captura permissões e grupos ms3
            permission_conn = PermissionConn(request.headers.get('Authorization'))
            response_user_perm_ms3 = permission_conn.get_permission_ms3(response_ms3.get('pk_user'))

            user_permissions_ms3 = response_user_perm_ms3.get('user_permissions')
            all_permissions_dict_ms3 = response_user_perm_ms3.get('all_permissions')

            if user_obj.is_superuser:
                perm_filter = ()
                perm_type = ()
            elif user_obj.is_staff:
                perm_filter = STAFF
                perm_type = ('delete',)
            elif user_obj.is_employee:
                perm_filter = EMPLOYEE
                perm_type = ('delete','add')
            elif user_obj.is_student:
                perm_filter = STUDENT
                perm_type = ('delete','change','add')

            user_groups_ms2 = {
                group.id: group.name for group in user_obj.groups.all()}
            user_permissions_ms2 = {
                permission.id: permission.name for permission in user_obj.user_permissions.all()}

            all_groups_ms2 = Group.objects.all()
            all_permissions_ms2 = Permission.objects.filter(
                ~Q(content_type__in=perm_filter))
            
            for type in perm_type:
                all_permissions_ms2 = all_permissions_ms2.filter(~Q(name__icontains=type))


            all_groups_dict_ms2 = {
                group.id: group.name for group in all_groups_ms2 if group.id not in user_groups_ms2}
            all_permissions_dict_ms2 = {
                permission.id: permission.name for permission in all_permissions_ms2}

            return Response({'groups': {
                'user_groups': user_groups_ms2,
                'all_groups': all_groups_dict_ms2},
                'ms2': {
                'user_permissions': user_permissions_ms2,
                'all_permissions': all_permissions_dict_ms2},
                'ms3': {
                'user_permissions': user_permissions_ms3,
                'all_permissions': all_permissions_dict_ms3
            }}, status=status.HTTP_200_OK)

        except Exception as error:
            message = 'Problemas ao visualizar Permission'
            logger.error({'results': message})
            logger.error(error)
            return Response({'results': message, 'error:':str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            data = request.data

            groups = [int(group_id) for group_id in data.get('groups').get('user_groups').keys()]
            user_perm_ms2 = [int(perm_ms2) for perm_ms2 in data.get('ms2').get('user_permissions').keys()]
            user_perm_ms3 = [int(perm_ms3) for perm_ms3 in data.get('ms3').get('user_permissions').keys()]

            user_obj, user_data = self.get_user_data(pk)
            if not user_obj:
                # Caso ocora algum erro, é retornado nesse return
                return user_data
            
            # filtra usuario ms3

            # captura permissões e grupos ms3

            is_superuser = False

            if user_obj.is_superuser:
                perm_filter = ()
                is_superuser = True
            elif user_obj.is_staff:
                perm_filter = STAFF
            elif user_obj.is_employee:
                perm_filter = EMPLOYEE
            elif user_obj.is_student:
                perm_filter = STUDENT

            user_groups_ms2 = [group.id for group in user_obj.groups.all()]
            user_permissions_ms2 = [
                permission.id for permission in user_obj.user_permissions.all()]
            
            user_permissions_ms3 = []
            
            # groups 
            user_groups_del = [group_id for group_id in user_groups_ms2 if group_id not in groups]
            user_groups_add = [group_id for group_id in groups if group_id not in user_groups_ms2]

            # permissions ms2 
            user_perm_ms2_del = [perm_ms2 for perm_ms2 in user_permissions_ms2 if perm_ms2 not in user_perm_ms2]
            user_perm_ms2_add = [perm_ms2 for perm_ms2 in user_perm_ms2 if perm_ms2 not in user_permissions_ms2]

            # permissions ms3 
            user_perm_ms3_del = [perm_ms3 for perm_ms3 in user_permissions_ms3 if perm_ms3 not in user_perm_ms3]
            user_perm_ms3_add = [perm_ms3 for perm_ms3 in user_perm_ms3 if perm_ms3 not in user_permissions_ms3]

            return Response({'results': 'serializer.data'}, status=status.HTTP_200_OK)

        except Exception as error:
            message = 'Problemas ao editar Permission'
            logger.error({'results': message})
            logger.error(error)
            return Response({'results': message, 'error:':str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
