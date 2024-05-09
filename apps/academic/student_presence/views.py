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
from apps.academic.student_presence.validations import validate_chosen_date, validate_employee_visualisation, validate_presence_percentage, validate_term_date
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

            # verifica se o usuario é o professor da turma para poder vlsualizar as presencas da turma
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

            # termo de acordo com a data escolhida
            term = school_year_date_info.get('fk_term')

            students_class, error = BSC.list_student_class(class_id)
            if error:
                return error
            # ids dos usuarios da turma
            user_ids = [student.get('fk_student_user')
                        for student in students_class]

            # verifica se a data atual corresponde ao termo escolhido
            # Caso não seja do termo, pode apenas visualizar as presencas enteriores, mas não editar
            editable = is_current_term = validate_term_date(school_year_date_info)

            presence = []
            presence = BSA.get_students_presence(
                pedagogical_setting_data.get('fk_subject'), class_id, term, chosen_date)

            # remove os alunos que não são da turma escolhida
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
                'presences': presence
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
            chosen_date =  request.GET.get("date", None)
            presences = data.get("presences", [])

            error = validate_chosen_date(chosen_date)
            if error:
                return error

            jwt_token = request.jwt_token
            user = request.user

            BCS = BaseClassSetting()
            BPS = BasePedagogicalSetting()
            BSC = BaseStudentClass()
            BSYD = BaseSchoolYearDate()
            BSA = BaseStudentPresence()

            class_setting_obj, error = BCS.get_object(class_id)
            if error:
                return error

            pedagogical_setting_obj, pedagogical_setting_data = BPS.get_pedagogical_setting_data(
                pedagogical_id)
            if not pedagogical_setting_obj:
                return pedagogical_setting_data


            # verifica se o usuario é o professor da turma para poder vlsualizar as presencas da turma
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
            
            # termo de acordo com a data escolhida
            term = school_year_date_info.get('fk_term')

            students_class, error = BSC.list_student_class(class_id)
            if error:
                return error
            # ids dos usuarios da turma
            user_ids = [student.get('fk_student_user')
                        for student in students_class]

            # verifica se a data atual corresponde ao termo escolhido
            # Caso não seja do termo, pode apenas visualizar as presencas enteriores, mas não editar
            editable = is_current_term = validate_term_date(school_year_date_info)

            # remove os alunos que não são da turma escolhida
            _ = [presences.remove(student_grade) for student_grade in deepcopy(presences)
                 if student_grade.get("fk_student_user") not in user_ids]
            

            if editable and is_current_term and presences:
                for presence in presences:
                    error = validate_presence_percentage(presence)
                    if error:
                        return error

                    StudentPresence.objects.filter(
                        pk_student_presence=presence.get("pk_student_presence"),
                        fk_class = class_id,
                        fk_term = term,
                        fk_subject = pedagogical_setting_data.get('fk_subject'),
                        fk_student_user = presence.get('fk_student_user')
                    ).update(
                        presence=presence.get("presence")
                    )
                return ResponseHelper.HTTP_200({'results': 'Presencas editadas com sucesso'})
            else:
                return ResponseHelper.HTTP_400({"detail": "Não é possivel editar as presencas nesse momento."})

        except Exception as error:
            message = 'Problemas ao editar StudentPresence'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
