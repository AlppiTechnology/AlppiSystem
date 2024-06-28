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
from apps.ct_requests.ct_ci_comment.ct_ci_comment import BaseCTCIComment
from apps.ct_requests.ct_ci_internal_note.ct_ci_internal_note import BaseCTCIInternalNote
from apps.ct_requests.ct_ci_internal_note.serializer import CTCIInternalNoteSerializer
from apps.ct_requests.ct_ci_regulament.ct_ci_regulament import BaseCTCIRegulament
from apps.ct_requests.ct_ci_student_internal_note.ct_ci_student_internal_note import BaseCTCIStudentInternalNote
from apps.ct_requests.models import CTCIInternalNote
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CTCIInternalNoteView(APIView, BaseCTCIInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            ct_ci_internal_note_obj, error = self.get_object(pk)
            if error:
                return error
            
            serializer = CTCIInternalNoteSerializer(ct_ci_internal_note_obj)
            return  ResponseHelper.HTTP_200({'results': serializer.data})

        except Exception as error:
            message = 'Problemas ao visualizar CTCIInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class UpdateCTCIInternalNoteView(APIView, BaseCTCIInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data

            ct_ci_internal_note_obj, error = self.get_object(pk)
            if error:
                return error

            serializer = CTCIInternalNoteSerializer(ct_ci_internal_note_obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar CTCIInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListCTCIInternalNoteView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            requests = CTCIInternalNote.objects.all()
            ct_ci_internal_note_paginate = self.paginate_queryset(
                requests, request, view=self)

            serializer = CTCIInternalNoteSerializer(
                ct_ci_internal_note_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)


        except Exception as error:
            message = 'Problemas ao listar todos os CTCIInternalNote.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CreateCTCIInternalNoteView(APIView):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data
            regulaments = data.pop('regulaments')
            students = data.pop('students')
            comment = data.pop('comment')
            user = request.user

            data['fk_campus'] = request.jwt_token.get('pk_campus')
            data['fk_reporter'] = user.pk_user
            data['created'] = datetime.now()
            data['updated'] = datetime.now()
            data['status'] = 1


            serializer = CTCIInternalNoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                salved_data = serializer.data

                BR= BaseCTCIRegulament()
                _, error = BR.create_pct_ci_regulament(salved_data.get('pk_ct_ci_internal_note'), regulaments)
                if error:
                    return error
                
                BIN = BaseCTCIStudentInternalNote()
                _, error = BIN.create_pct_ci_student_internal_note(salved_data.get('pk_ct_ci_internal_note'), students)
                if error:
                    return error
                
                BC = BaseCTCIComment()
                _, error = BC.create_pct_ci_comment(salved_data.get('pk_ct_ci_internal_note'), comment, user.pk_user)
                if error:
                    return error
                
                return  ResponseHelper.HTTP_201({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar CTCIInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteCTCIInternalNoteView(APIView, BaseCTCIInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            ct_ci_internal_note_obj, error = self.get_object(pk)
            if error:
                return error
            
            ct_ci_internal_note_obj.delete()
            return  ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar CTCIInternalNote'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ChangeStatusCTCIInternalNoteView(APIView, BaseCTCIInternalNote):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]
    
    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            ct_ci_internal_note_obj, error = self.get_object(pk)
            if error:
                return error

            ct_ci_internal_note_obj.is_active = data.get('is_active')
            ct_ci_internal_note_obj.save()
            logger.info('Alterando status do request para {}.'.format(data.get('is_active')))

            message = 'CTCIInternalNote atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do request'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})