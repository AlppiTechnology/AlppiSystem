#!/usr/bin/python
# -*- encoding: utf-8 -*-
from copy import deepcopy
import os
import logging

from datetime import datetime, date
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import HasPermission, IsViewAllowed
from alppi.responses import ResponseHelper
from alppi.utils.decorators import permission_required
from alppi.utils.groups import TEACHER
from apps.academic.class_setting.class_setting import BaseClassSetting
from apps.academic.models import StudentPresence
from apps.academic.pedagogical_setting.pedagogical_setting import BasePedagogicalSetting
from apps.academic.school_year_date.school_year_date import BaseSchoolYearDate
from apps.academic.student_class.student_class import BaseStudentClass
from apps.academic.student_presence.serializer import StudentPresenceSerializer
from apps.academic.student_presence.student_presence import BaseStudentPresence
from apps.academic.student_presence.validations import validate_chosen_date, validate_employee_visualisation, validate_term_date
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')


@method_decorator(permission_required(TEACHER), name='dispatch')
class StudentPresenceView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, class_id, pedagogical_id, format=None) -> ResponseHelper:

        try:
            chosen_date =  request.GET.get("date", None)

            error = validate_chosen_date(chosen_date)
            if error:
                return error

            BCS = BaseClassSetting()
            BPS = BasePedagogicalSetting()
            BSC = BaseStudentClass()
            BSYD = BaseSchoolYearDate()
            BSA = BaseStudentPresence()

            jwt_token = request.jwt_token
            user = request.user

            class_setting_obj, error = BCS.get_object(class_id)
            if error:
                return error

            pedagogical_setting_obj, pedagogical_setting_data = BPS.get_pedagogical_setting_data(
                pedagogical_id)
            if not pedagogical_setting_obj:
                return pedagogical_setting_data

            # verifica se o usuario é o professor da turma para poder vlsualizar as notas da turma
            if jwt_token.get('group') not in ('superuser', 'administrador'):
                employee_visualisation_error = validate_employee_visualisation(
                    pedagogical_setting_data, user.pk_user)
                if employee_visualisation_error:
                    return employee_visualisation_error

            # dados do termo de acordo com data escolhida
            school_year_date_info, error = BSYD.get_school_year_date_by_date(
                class_setting_obj.fk_school_year, chosen_date)
            if error:
                return error

            # termo do
            term = school_year_date_info.get('fk_term')

            students_class, error = BSC.list_student_class(class_id)
            if error:
                return error
            # ids dos usuarios da turma
            user_ids = [student.get('fk_student_user')
                        for student in students_class]

            # verifica se a data atual corresponde ao termo escolhido
            # Caso não seja do termo, pode apenas visualizar as notas enteriores, mas não editar
            editable = is_current_term = validate_term_date(school_year_date_info)

            presence = []
            presence = BSA.get_students_presence(
                pedagogical_setting_data.get('fk_subject'), class_id, term, chosen_date)

            _ = [user_ids.remove(presence_item.get('fk_student_user')) for
                 presence_item in presence if presence_item.get('fk_student_user') in user_ids]

            # if is_current_term:
            for studet in user_ids:
                if is_current_term:
                    student_presence = BSA.build_student_presence_data(
                        user_id=studet,
                        class_id=class_id,
                        term_id=term,
                        subject_id=pedagogical_setting_data.get('fk_subject'),
                        chosen_date=chosen_date)

                    student_presence_created, create_error = BSA.create_student_presence(
                        student_presence)
                    if create_error:
                        return create_error

                    presence.append(student_presence_created)

            logger.info('Retornando nota dos alunos.')
            return ResponseHelper.HTTP_200({
                'editable': editable,
                'skill': class_setting_obj.skill,
                'presence': presence
            })

        except Exception as error:
            message = 'Problemas ao visualizar StudentPresence'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(TEACHER), name='dispatch')
class UpdateStudentPresenceView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, class_id, pedagogical_id, format=None) -> ResponseHelper:
        try:
            data = request.data
            term = int(request.GET.get("term", '1'))
            presence = data.get("presence", [])

            jwt_token = request.jwt_token
            user = request.user

            BCS = BaseClassSetting()
            BPS = BasePedagogicalSetting()
            BSC = BaseStudentClass()
            BSYD = BaseSchoolYearDate()

            class_setting_obj, error = BCS.get_object(class_id)
            if error:
                return error

            pedagogical_setting_obj, pedagogical_setting_data = BPS.get_pedagogical_setting_data(
                pedagogical_id)
            if not pedagogical_setting_obj:
                return pedagogical_setting_data

            # verifica se o usuario é o professor da turma para poder vlsualizar as notas da turma
            if jwt_token.get('group') not in ('superuser', 'administrador'):
                employee_visualisation_error = validate_employee_visualisation(
                    pedagogical_setting_data, user.pk_user)
                if employee_visualisation_error:
                    return employee_visualisation_error

            school_year_date_info, error = BSYD.get_school_year_date_info(
                class_setting_obj.fk_school_year, term)
            if error:
                return error

            # Nota maxima do termo da turma
            term_grade = school_year_date_info.get('grade')

            students_class, error = BSC.list_student_class(class_id)
            if error:
                return error
            # ids dos usuarios da turma
            user_ids = [student.get('fk_student_user')
                        for student in students_class]

            # verifica se a data atual corresponde ao termo escolhido
            # Caso não seja do termo, pode apenas visualizar as notas enteriores, mas não editar
            editable = is_current_term = validate_term_date(school_year_date_info)

            _ = [presence.remove(student_grade) for student_grade in deepcopy(presence)
                 if student_grade.get("fk_student_user") not in user_ids]

            if editable and is_current_term and presence:
                for grade in presence:
                    error = valeidate_sum_presence(grade, term_grade)
                    if error:
                        return error

                    StudentPresence.objects.filter(
                        pk_student_presence=grade.get("pk_student_presence")
                    ).update(
                        edited=datetime.now(),
                        grade_1=grade.get('grade_1'),
                        grade_2=grade.get('grade_2'),
                        grade_3=grade.get('grade_3'),
                        grade_4=grade.get('grade_4'),
                        grade_5=grade.get('grade_5'),
                    )
                return ResponseHelper.HTTP_200({'results': 'Notas editadas com sucesso'})
            else:
                return ResponseHelper.HTTP_400({"detail": "Não é possivel editar as notas nesse momento."})

        except Exception as error:
            message = 'Problemas ao editar StudentPresence'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(TEACHER), name='dispatch')
class DeleteStudentPresenceView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            student_presence_obj, error = self.get_object(pk)
            if error:
                return error

            student_presence_obj.delete()
            return ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar StudentPresence'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(TEACHER), name='dispatch')
class ListStudentPresenceView(APIView, CustomPagination):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            student_presences = StudentPresence.objects.all()
            student_presence_paginate = self.paginate_queryset(
                student_presences, request, view=self)

            serializer = StudentPresenceSerializer(
                student_presence_paginate, many=True)
            return ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)

        except Exception as error:
            message = 'Problemas ao listar todos os StudentPresence.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(TEACHER), name='dispatch')
class CreateStudentPresenceView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data

            serializer = StudentPresenceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return ResponseHelper.HTTP_201({'results': serializer.data})

            return ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar StudentPresence'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(TEACHER), name='dispatch')
class ChangeStatusStudentPresenceView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            student_presence_obj, error = self.get_object(pk)
            if error:
                return error

            student_presence_obj.is_active = data.get('is_active')
            student_presence_obj.save()
            logger.info('Alterando status do student_presence para {}.'.format(
                data.get('is_active')))

            message = 'StudentPresence atualizado com sucesso.'
            return ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do student_presence'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
