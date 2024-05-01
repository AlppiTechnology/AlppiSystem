#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from datetime import datetime
from django.db.models import Q, F

from alppi.responses import ResponseHelper
from apps.academic.models import PedagogicalSetting
from apps.academic.pedagogical_setting.serializer import PedagogicalSettingSerializer
from apps.academic.pedagogical_setting.validations import validate_pedagogical_updates, validate_repeated_subject


logger = logging.getLogger('django')


class BasePedagogicalSetting():

    def get_object(self, pk) -> tuple:
        try:
            return (PedagogicalSetting.objects.get(pk=pk), None)
        except PedagogicalSetting.DoesNotExist:
            message = 'Não foi possivel encontrar este PedagogicalSetting.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (PedagogicalSetting.objects.all(), None)
        except PedagogicalSetting.DoesNotExist:
            message = 'Não foi possivel encontrar todos os PedagogicalSetting.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_pedagogical_setting_data(self, pk) -> tuple:
        """
            Captura os id da pedagogical_setting e dados serializados de um pedagogical_setting especifica
        """
        logger.info(f'Capturando dados do pedagogical_setting id:{pk}')
        pedagogical_setting_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = PedagogicalSettingSerializer(pedagogical_setting_id)
        return pedagogical_setting_id, selrializer.data

    def list_pedagogical_setting(self, fk_class_setting:int):

        try:
            pedagogical_setting_obj = PedagogicalSetting.objects.annotate(
                subject_name=F('fk_subject__subject_name'),
                employee_name =F('fk_employee_user__username')
            ).filter(
                fk_class_setting=fk_class_setting,
                status = True
            ).values('pk_pedagogical_setting','fk_subject','subject_name'
                     ,'fk_employee_user','employee_name'
            ).order_by('subject_name')

            if pedagogical_setting_obj:
                return list(pedagogical_setting_obj), None

            return [], None

        except Exception as error:
            message = 'Problemas ao listar StudentClass'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def create_pedagogical_setting(self, pedagogical:dict, fk_class_setting:int):
        try:
             # verifica se existe disciplinas repetidas
            repeated_subject = validate_repeated_subject(pedagogical)
            if repeated_subject:
                return None, repeated_subject

            for data in pedagogical:

                data['fk_class_setting'] = fk_class_setting
                data['edited'] = datetime.now()
                data['status'] = 1

                serializer = PedagogicalSettingSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                else:
                    return  (None, ResponseHelper.HTTP_404({'detail': serializer.errors}))
            return None, None

        except PedagogicalSetting.DoesNotExist:
            message = 'Não foi possivel encontrar todos os PedagogicalSetting.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def update_pedagogical_setting(self, pedagogical_list:dict, fk_class_setting:int):
        try:

            pedagogical_setting_old = PedagogicalSetting.objects.annotate(
            ).filter(
                fk_class_setting=fk_class_setting,
                status=True
            ).values('pk_pedagogical_setting','fk_subject',
                     'fk_employee_user')

            if pedagogical_setting_old:
                pedagogical_setting_old = list(pedagogical_setting_old)

            else:
                pedagogical_setting_old = []

            to_delete, to_update, to_add = validate_pedagogical_updates(pedagogical_setting_old, pedagogical_list)

            # Não pode deletar pois existe a relação entre as tabelas, então
            # somente e desativado.
            for pedagogical_delete in to_delete:

                pedagogical_setting_obj, error = self.get_object(pedagogical_delete)
                if error: 
                    return None, error

                pedagogical_setting_obj.status = False
                pedagogical_setting_obj.save()

            # Atualiza os pedagogical settings existentes
            for pedagogical_update in to_update:

                pedagogical_setting_obj, pedagogical_setting_data = self.get_pedagogical_setting_data(
                    pedagogical_update.get('pk_pedagogical_setting'))

                if not pedagogical_setting_obj:
                    return None, pedagogical_setting_data

                pedagogical_update['fk_subject'] = pedagogical_setting_data.get('fk_subject')
                pedagogical_update['fk_class_setting'] = pedagogical_setting_data.get('fk_class_setting')
                pedagogical_update['edited'] = datetime.now()
                pedagogical_update['status'] = pedagogical_setting_data.get('status')

                serializer = PedagogicalSettingSerializer(pedagogical_setting_obj,
                                                            data=pedagogical_update)
                if serializer.is_valid():
                    serializer.save()

                else:
                    return None, ResponseHelper.HTTP_400({'detail':serializer.errors})

            # Adiciona novos pedagogical_setting
            if to_add:
                _, error = self.create_pedagogical_setting(to_add, fk_class_setting)
                if error:
                    return None, error
                
            return None, None

        except Exception as error:
            message = 'Problemas ao Atualizar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def delete_pedagogical_setting(self, fk_class_setting:int):
        try:
            pedagogical_setting_obj = PedagogicalSetting.objects.filter(
                fk_class_setting=fk_class_setting)

            pedagogical_setting_obj.delete()

            return None, None

        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def change_status_all_pedagogical_setting(self, fk_class_setting:int, changed_status:int):
        try:
            pedagogical_setting_objs = PedagogicalSetting.objects.filter(
                fk_class_setting=fk_class_setting)

            for pedagogical_setting_obj in pedagogical_setting_objs:
                pedagogical_setting_obj.status = changed_status
                pedagogical_setting_obj.save()

            return None, None

        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})