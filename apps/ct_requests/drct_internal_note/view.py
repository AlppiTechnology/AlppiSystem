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
from apps.ct_requests.drct_comment.drct_comment import BaseDRCTComment
from apps.ct_requests.drct_internal_note.drct_internal_note import BaseDRCTInternalNote
from apps.ct_requests.drct_internal_note.serializer import DRCTInternalNoteSerializer
from apps.ct_requests.drct_regulament.drct_regulament import BaseDRCTRegulament
from apps.ct_requests.drct_student_internal_note.drct_student_internal_note import BaseDRCTStudentInternalNote
from apps.ct_requests.models import DRCTInternalNote
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DRCTInternalNoteView(APIView, BaseDRCTInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            drct_internal_note_obj, error = self.get_object(pk)
            if error:
                return error
            
            serializer = DRCTInternalNoteSerializer(drct_internal_note_obj)
            return  ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar DRCTInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class UpdateDRCTInternalNoteView(APIView, BaseDRCTInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data

            drct_internal_note_obj, error = self.get_object(pk)
            if error:
                return error

            serializer = DRCTInternalNoteSerializer(drct_internal_note_obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar DRCTInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListDRCTInternalNoteView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            requests = DRCTInternalNote.objects.all()
            drct_internal_note_paginate = self.paginate_queryset(
                requests, request, view=self)

            serializer = DRCTInternalNoteSerializer(
                drct_internal_note_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)


        except Exception as error:
            message = 'Problemas ao listar todos os DRCTInternalNote.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CreateDRCTInternalNoteView(APIView):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data
            regulaments = data.pop('regulaments')
            students = data.pop('students')
            comment = data.pop('comments')
            user = request.user

            data['fk_campus'] = request.jwt_token.get('pk_campus')
            data['fk_reporter'] = user.pk_user
            data['created'] = datetime.now()
            data['created'] = datetime.now()
            data['status'] = 1


            serializer = DRCTInternalNoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                salved_data = serializer.data

                BR= BaseDRCTRegulament()
                _, error = BR.create_pdrct_regulament(salved_data.get('pk_internal_note'), regulaments)
                if error:
                    return error
                
                BIN = BaseDRCTStudentInternalNote()
                _, error = BIN.create_pdrct_student_internal_note(salved_data.get('pk_internal_note'), regulaments)
                if error:
                    return error
                
                BC = BaseDRCTComment()
                _, error = BC.create_pdrct_comment(salved_data.get('pk_internal_note'), comment, user.pk_user)
                if error:
                    return error
                
                return  ResponseHelper.HTTP_201({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar DRCTInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteDRCTInternalNoteView(APIView, BaseDRCTInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            drct_internal_note_obj, error = self.get_object(pk)
            if error:
                return error
            
            drct_internal_note_obj.delete()
            return  ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar DRCTInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ChangeStatusDRCTInternalNoteView(APIView, BaseDRCTInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]
    
    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            drct_internal_note_obj, error = self.get_object(pk)
            if error:
                return error

            drct_internal_note_obj.is_active = data.get('is_active')
            drct_internal_note_obj.save()
            logger.info('Alterando status do request para {}.'.format(data.get('is_active')))

            message = 'DRCTInternalNote atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do request'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})