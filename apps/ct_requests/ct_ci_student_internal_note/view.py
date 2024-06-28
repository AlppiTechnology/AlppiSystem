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
from apps.ct_requests.ct_ci_student_internal_note.ct_ci_student_internal_note import BaseCTCIStudentInternalNote
from apps.ct_requests.ct_ci_student_internal_note.serializer import CTCIStudentInternalNoteSerializer
from apps.ct_requests.models import CTCIStudentInternalNote
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CTCIStudentInternalNoteView(APIView, BaseCTCIStudentInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            ct_ci_student_internal_note_obj, error = self.get_object(pk)
            if error:
                return error
            
            serializer = CTCIStudentInternalNoteSerializer(ct_ci_student_internal_note_obj)
            return  ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar CTCIStudentInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class UpdateCTCIStudentInternalNoteView(APIView, BaseCTCIStudentInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data

            ct_ci_student_internal_note_obj, error = self.get_object(pk)
            if error:
                return error

            serializer = CTCIStudentInternalNoteSerializer(ct_ci_student_internal_note_obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar CTCIStudentInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListCTCIStudentInternalNoteView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            student_internal_note = CTCIStudentInternalNote.objects.all()
            ct_ci_student_internal_note_paginate = self.paginate_queryset(
                student_internal_note, request, view=self)

            serializer = CTCIStudentInternalNoteSerializer(
                ct_ci_student_internal_note_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)


        except Exception as error:
            message = 'Problemas ao listar todos os CTCIStudentInternalNote.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CreateCTCIStudentInternalNoteView(APIView):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data

            serializer = CTCIStudentInternalNoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_201({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar CTCIStudentInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteCTCIStudentInternalNoteView(APIView, BaseCTCIStudentInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            ct_ci_student_internal_note_obj, error = self.get_object(pk)
            if error:
                return error
            
            ct_ci_student_internal_note_obj.delete()
            return  ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar CTCIStudentInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ChangeStatusCTCIStudentInternalNoteView(APIView, BaseCTCIStudentInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]
    
    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            ct_ci_student_internal_note_obj, error = self.get_object(pk)
            if error:
                return error

            ct_ci_student_internal_note_obj.is_active = data.get('is_active')
            ct_ci_student_internal_note_obj.save()
            logger.info('Alterando status do request para {}.'.format(data.get('is_active')))

            message = 'CTCIStudentInternalNote atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do request'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})