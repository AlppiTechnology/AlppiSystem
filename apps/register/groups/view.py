#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging

from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import  HasPermission, IsViewAllowed
from alppi.utils.decorators import  permission_required
from alppi.utils.groups import ADMINISTRATOR, SUPERUSER
from apps.register.groups.serializer import GroupSerializer


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class GroupsView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None):

        try:

            groups = Group.objects.all()

            # groups_name = {group.id: group.name for group in groups}
            groups_name = [group.name.title() for group in groups]

            return Response({'groups': groups_name}, status=status.HTTP_200_OK)

        except Exception as error:
            message = 'Problemas ao visualizar Permission'
            logger.error({'results': message})
            logger.error(error)
            return Response({'results': message, 'error:':str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@method_decorator(permission_required(SUPERUSER), name='dispatch')
class UpdateGroupsView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None):
        try:
            data = request.data

            return Response({'results': 'serializer.data'}, status=status.HTTP_200_OK)

        except Exception as error:
            message = 'Problemas ao editar Permission'
            logger.error({'results': message})
            logger.error(error)
            return Response({'results': message, 'error:':str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CreateGroupsView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None):
        try:
            data = {}
            data['name'] = request.data.get('name').lower()
            serializer = GroupSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                return Response({'results': serializer.data}, status=status.HTTP_201_CREATED)

            return Response({'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            message = 'Problemas ao cadastrar Campus'
            logger.error({'results': message})
            logger.error(error)
            return Response({'results': message, 'error:':str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)