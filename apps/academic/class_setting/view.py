#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging

from datetime import datetime
from django.db.models import Q, F
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import HasPermission, IsViewAllowed
from alppi.responses import ResponseHelper
from alppi.utils.decorators import permission_required
from alppi.utils.groups import SUPERUSER
from apps.academic.models import ClassSetting
from apps.academic.class_setting.class_setting import BaseClassSetting
from apps.academic.class_setting.serializer import ClassSettingSerializer
from apps.academic.pedagogical_setting.pedagogical_setting import BasePedagogicalSetting
from apps.academic.student_class.student_class import BaseStudentClass
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ClassSettingView(APIView, BaseClassSetting):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, pk, format=None) -> ResponseHelper:

        try:
            class_setting_obj, class_setting_data = self.get_class_setting_data(pk)
            if not class_setting_obj:
                return class_setting_data
            
            BPS = BasePedagogicalSetting()
            pedagogical, error = BPS.list_pedagogical_setting(class_setting_data.get('pk_class_setting'))
            if error:
                return error
            class_setting_data['pedagogical'] = pedagogical


            BSC = BaseStudentClass()
            studets, error = BSC.list_student_class(class_setting_data.get('pk_class_setting'))
            if error:
                return error
            class_setting_data['students'] = studets
            
            return  ResponseHelper.HTTP_200({'results': class_setting_data})

        except Exception as error:
            message = 'Problemas ao visualizar ClassSetting'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class UpdateClassSettingView(APIView, BaseClassSetting):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            pedagogical = data.pop('pedagogical')
            students = data.pop('students')

            class_setting_obj, class_setting_data = self.get_class_setting_data(pk)
            if not class_setting_obj:
                return class_setting_data
            
            data['fk_campus'] = class_setting_data.get('fk_campus')
            data['edited'] = datetime.now()
            salved_data = {}

            serializer = ClassSettingSerializer(class_setting_obj, data=data)
            if serializer.is_valid():
                # serializer.save()


                BPS = BasePedagogicalSetting()
                _, error = BPS.update_pedagogical_setting(pedagogical, pk)
                if error:
                    return error
                
                BSC = BaseStudentClass()
                _, error = BSC.update_student_class(students, pk)
                if error:
                    return error


                return  ResponseHelper.HTTP_200({'results': serializer.data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao editar ClassSetting'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteClassSettingView(APIView, BaseClassSetting):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            class_setting_obj, error = self.get_object(pk)
            if error:
                return error
            
            # BPS = BasePedagogicalSetting()
            # _, error = BPS.delete_pedagogical_setting(pk)
            # if error:
            #     return error

            # BSC = BaseStudentClass()
            # _, error = BSC.delete_student_class(pk)
            # if error:
            #     return error
            
            class_setting_obj.delete()
            return  ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar ClassSetting'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListClassSettingView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            year = request.GET.get('year',None)
            search_status = request.GET.get('status', None)
            class_name = request.GET.get('class_name',None)
            fk_school_grade = request.GET.get('school_grade',None)

            class_settings = ClassSetting.objects.filter(
                ).annotate(
                    school_grade_name=F('fk_school_grade__name'),
                    school_year_name=F('fk_school_year__year'),
                    school_level_name=F('fk_school_grade__fk_school_level__name')
                ).values('pk_class_setting','name','fk_school_grade',
                         'school_grade_name','school_level_name','fk_school_year',
                         'school_year_name','status'
                ).order_by('name','fk_school_grade')

            if year:
                class_settings = class_settings.filter(fk_school_year = year)

            if search_status:
                class_settings = class_settings.filter(status = search_status)

            if class_name:
                class_settings = class_settings.filter(name = class_name)

            if fk_school_grade:
                class_settings = class_settings.filter(fk_school_grade = fk_school_grade)

            class_setting_paginate = self.paginate_queryset(
                class_settings, request, view=self)


            return  ResponseHelper.HTTP_200(self.get_paginated_response(class_setting_paginate).data)


        except Exception as error:
            message = 'Problemas ao listar todos os ClassSetting.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
        

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CreateClassSettingView(APIView):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data

            pedagogical = data.pop('pedagogical')
            students = data.pop('students')


            data['fk_campus'] = request.jwt_token.get('pk_campus')
            data['edited'] = datetime.now()
            data['status'] = 1
            salved_data = {}

            serializer = ClassSettingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                salved_data = serializer.data

                BPS = BasePedagogicalSetting()
                _, error = BPS.create_pedagogical_setting(pedagogical, salved_data.get('pk_class_setting'))
                if error:
                    return error
                
                BSC = BaseStudentClass()
                _, error = BSC.create_student_class(students, salved_data.get('pk_class_setting'))
                if error:
                    return error

                return  ResponseHelper.HTTP_201({'results': salved_data})

            return  ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            if salved_data.get('pk_class_setting'):
                BPS.delete_pedagogical_setting(salved_data.get('pk_class_setting'))
                BSC.delete_student_class(salved_data.get('pk_class_setting'))

            message = 'Problemas ao cadastrar ClassSetting'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ChangeStatusClassSettingView(APIView, BaseClassSetting):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]
    
    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            class_setting_obj, error = self.get_object(pk)
            if error:
                return error
            
            changed_status = data.get('status')
            
            BPS = BasePedagogicalSetting()
            _, error = BPS.change_status_all_pedagogical_setting(pk, changed_status)
            if error:
                return error

            BSC = BaseStudentClass()
            _, error = BSC.change_status_all_student_classg(pk, changed_status)
            if error:
                return error

            class_setting_obj.status = changed_status
            class_setting_obj.save()
            logger.info('Alterando status do class_setting para {}.'.format(data.get('is_active')))

            message = 'ClassSetting atualizado com sucesso.'
            return  ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do class_setting'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})