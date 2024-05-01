#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.academic.models import ClassSetting
from apps.academic.class_setting.serializer import ClassSettingSerializer


logger = logging.getLogger('django')


class BaseClassSetting():

    def get_object(self, pk) -> tuple:
        try:
            return (ClassSetting.objects.get(pk=pk), None)
        except ClassSetting.DoesNotExist:
            message = 'Não foi possivel encontrar este ClassSetting.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (ClassSetting.objects.all(), None)
        except ClassSetting.DoesNotExist:
            message = 'Não foi possivel encontrar todos os ClassSetting.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_class_setting_data(self, pk) -> tuple:
        """
            Captura os id da class_setting e dados serializados de um class_setting especifica
        """
        logger.info(f'Capturando dados do class_setting id:{pk}')
        class_setting_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = ClassSettingSerializer(class_setting_id)
        return class_setting_id, selrializer.data
