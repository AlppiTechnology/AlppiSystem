#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import DRCTStudentRequest
from apps.ct_requests.drct_student_request.serializer import DRCTStudentRequestSerializer


logger = logging.getLogger('django')


class BaseDRCTStudentRequest():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTStudentRequest.objects.get(pk=pk), None)
        except DRCTStudentRequest.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTStudentRequest.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTStudentRequest.objects.all(), None)
        except DRCTStudentRequest.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTStudentRequest.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_student_request_data(self, pk) -> tuple:
        """
            Captura os id da drct_student_request e dados serializados de um drct_student_request especifica
        """
        logger.info(f'Capturando dados do drct_student_request id:{pk}')
        drct_student_request_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTStudentRequestSerializer(drct_student_request_id)
        return drct_student_request_id, selrializer.data
