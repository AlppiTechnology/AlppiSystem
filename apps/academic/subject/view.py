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
from apps.academic.subject.subject import BaseSubject
from apps.academic.subject.serializer import SubjectSerializer
from apps.academic.models import Subject
from apps.academic.subject.validations import validate_subject_area, validate_subject_name

from common.pagination.pagination import CustomPagination
from common.util import uppercase_first



logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class SubjectView(APIView, BaseSubject):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            subject_obj, error = self.get_object(pk)
            if error:
                return error
            
            serializer = SubjectSerializer(subject_obj)
            return ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar Subject'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ListSubjectView(APIView, BaseSubject, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:

        try:
            search_subject = request.GET.get('subject', None)
            search_status = request.GET.get('status', '1')
            
            fk_campus = request.jwt_token.get('pk_campus')

            subject = Subject.objects.filter(fk_campus=fk_campus
                                ).values('pk_subject','subject_name', 'subject_code', 'status')

            # filtra deacordo com a subject pessada por parametro
            if search_subject:
                subject = subject.filter(subject_name__icontains=search_subject)

            # filtra de acordo com o status passado por parametro
            if search_status:
                subject = subject.filter(status=search_status)

            # Ordenando por status e nome
            subject = subject.order_by('-status', 'subject_name')

            subject_paginate = self.paginate_queryset(subject, request, view=self)

            return ResponseHelper.HTTP_200(self.get_paginated_response(subject_paginate).data)


        except Exception as error:
            message = 'Problemas ao visualizar Subject'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class UpdateSubjectView(APIView, BaseSubject):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data

            subject_obj, subject_data = self.get_subject_data(pk)
            if not subject_obj:
                return subject_data
            
            assert validate_subject_name(data)

            subject_data['edited'] = datetime.now()
            subject_data['subject_name'] = data.get('subject_name')
            subject_data['status'] = 1 if data.get('status') else 0

            # deixa as primeiras letras dos nomes maiusculas
            uppercase_first(subject_data, ['subject_name'])

            serializer = SubjectSerializer(subject_obj, data=subject_data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar Subject Area'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteSubjectView(APIView, BaseSubject):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            subject_obj, error = self.get_object(pk)
            if error:
                return error
            
            subject_obj.delete()
            return  ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar Subject'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class CreateSubjectView(APIView):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data

            assert validate_subject_name(data)
            assert validate_subject_area(data)

            data['fk_campus'] = request.jwt_token.get('pk_campus')
            data['edited'] = datetime.now()
            data['status'] = 1

            # deixa as primeiras letras dos nomes maiusculas
            uppercase_first(data, ['subject_name'])

            # capturando ultimo codigo cadastrado
            last_subject_code = Subject.objects.filter(
                    fk_campus=data.get('fk_campus')).order_by('-subject_code').first()
            
            # Caso seja o primeiro codigo, iniciará com 1000
            if not last_subject_code:
                    data['subject_code'] = '1000'

            else:
                # novo codigo criado a partir do ultimo dacastrado
                new_subject_code = int(last_subject_code.subject_code)+1
                data['subject_code'] = str(new_subject_code)

            serializer = SubjectSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f'Disciplina cadastrada com sucesso')
                return  ResponseHelper.HTTP_201({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar Subject Area'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(ADMINISTRATOR), name='dispatch')
class ChangeStatusSubjectView(APIView, BaseSubject):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]
    
    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            subject_obj, error = self.get_object(pk)
            if error:
                return error

            subject_obj.status = data.get('status')
            subject_obj.save()
            logger.info('Alterando status do subject para {}.'.format(data.get('is_active')))

            message = 'Disciplina atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do subject'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})