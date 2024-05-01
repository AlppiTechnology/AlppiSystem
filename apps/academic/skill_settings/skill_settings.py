#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.academic.models import SkillSettings
from apps.academic.skill_settings.serializer import SkillSettingsSerializer


logger = logging.getLogger('django')


class BaseSkillSettings():

    def get_object(self, pk) -> tuple:
        try:
            return (SkillSettings.objects.get(pk=pk), None)
        except SkillSettings.DoesNotExist:
            message = 'Não foi possivel encontrar este SkillSettings.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (SkillSettings.objects.all(), None)
        except SkillSettings.DoesNotExist:
            message = 'Não foi possivel encontrar todos os SkillSettings.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_skill_settings_data(self, pk) -> tuple:
        """
            Captura os id da skill settings e dados serializados de um skill settings especifica
        """
        logger.info(f'Capturando dados do skill settings id:{pk}')
        skill_settings_obj, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = SkillSettingsSerializer(skill_settings_obj)
        return skill_settings_obj, selrializer.data
