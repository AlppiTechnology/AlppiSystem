#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper

from apps.register.models import User
from apps.register.student.serializer import StudentSerializer


logger = logging.getLogger('django')


class BaseStudent():

    def get_object(self, pk) -> tuple:
        try:
            return (User.objects.get(pk=pk), None)
        except User.DoesNotExist:
            message = 'Não foi possivel encontrar este Estudante.'
            logger.error({'results': message})
            return None, ResponseHelper.HTTP_404({'results': message})


    def get_all_object(self) -> tuple:
        try:
            return (User.objects.all(), None)
        except User.DoesNotExist:
            message = 'Não foi possivel encontrar todos os Estudante.'
            logger.error({'results': message})
            return None, ResponseHelper.HTTP_404({'results': message})


    def get_student_data(self, pk) -> tuple:
        """
            Captura os id da student e dados serializados de um student especifica
        """
        logger.info(f'Capturando dados do student id:{pk}')
        student_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = StudentSerializer(student_id)
        return student_id, selrializer.data

    def get_last_registration(self):
        logger.info(f'Capturando o ultimo numero de matricula cadastrada')
        last_registration = User.objects.all().order_by('-registration').first()

        if not last_registration:
            return '00001'

        new_registration = int(last_registration.registration)+1

        return str(new_registration).zfill(5)

    def check_registration(self, registration):
        logger.info(f'Verificando se existe matricula ja cadastrada.')
        student_registration = User.objects.filter(registration=registration)
        serializer = StudentSerializer(student_registration, many=True)

        if serializer.data:
            message = 'Numero de registration ja cadastrada!'
            logger.error({'results': message})
            return ResponseHelper.HTTP_404({'results': message})

        return None
