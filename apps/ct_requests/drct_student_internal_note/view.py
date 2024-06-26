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
from apps.ct_requests.drct_student_internal_note.drct_student_internal_note import BaseDRCTStudentInternalNote
from apps.ct_requests.drct_student_internal_note.serializer import DRCTStudentInternalNoteSerializer
from apps.ct_requests.models import DRCTStudentInternalNote
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DRCTStudentInternalNoteView(APIView, BaseDRCTStudentInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            drct_student_internal_note_obj, error = self.get_object(pk)
            if error:
                return error
            
            serializer = DRCTStudentInternalNoteSerializer(drct_student_internal_note_obj)
            return  ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar DRCTStudentInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class UpdateDRCTStudentInternalNoteView(APIView, BaseDRCTStudentInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data

            drct_student_internal_note_obj, error = self.get_object(pk)
            if error:
                return error

            serializer = DRCTStudentInternalNoteSerializer(drct_student_internal_note_obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar DRCTStudentInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListDRCTStudentInternalNoteView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            student_internal_note = DRCTStudentInternalNote.objects.all()
            drct_student_internal_note_paginate = self.paginate_queryset(
                student_internal_note, request, view=self)

            serializer = DRCTStudentInternalNoteSerializer(
                drct_student_internal_note_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)


        except Exception as error:
            message = 'Problemas ao listar todos os DRCTStudentInternalNote.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CreateDRCTStudentInternalNoteView(APIView):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data

            serializer = DRCTStudentInternalNoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_201({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar DRCTStudentInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteDRCTStudentInternalNoteView(APIView, BaseDRCTStudentInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            drct_student_internal_note_obj, error = self.get_object(pk)
            if error:
                return error
            
            drct_student_internal_note_obj.delete()
            return  ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar DRCTStudentInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ChangeStatusDRCTStudentInternalNoteView(APIView, BaseDRCTStudentInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]
    
    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            drct_student_internal_note_obj, error = self.get_object(pk)
            if error:
                return error

            drct_student_internal_note_obj.is_active = data.get('is_active')
            drct_student_internal_note_obj.save()
            logger.info('Alterando status do request para {}.'.format(data.get('is_active')))

            message = 'DRCTStudentInternalNote atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do request'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})