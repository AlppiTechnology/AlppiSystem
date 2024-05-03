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
from apps.academic.models import SubjectGrade
from apps.academic.pedagogical_setting.pedagogical_setting import BasePedagogicalSetting
from apps.academic.school_year_date.school_year_date import BaseSchoolYearDate
from apps.academic.student_class.student_class import BaseStudentClass
from apps.academic.subject_grade.serializer import SubjectGradeSerializer
from apps.academic.subject_grade.subject_grade import BaseSubjectGrade
from apps.academic.subject_grade.validations import valeidate_sum_grades, validate_employee_visualisation, validate_term_date
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')


@method_decorator(permission_required(TEACHER), name='dispatch')
class SubjectGradeView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, class_id, pedagogical_id, format=None) -> ResponseHelper:

        try:
            term = int(request.GET.get("term", '1'))
            BCS = BaseClassSetting()
            BPS = BasePedagogicalSetting()
            BSC = BaseStudentClass()
            BSYD = BaseSchoolYearDate()
            BSG = BaseSubjectGrade()

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

            school_year_date_info, error = BSYD.get_school_year_date_info(
                class_setting_obj.fk_school_year, term)
            if error:
                return error

            # Verifica se a data atual e menor que o inicio do periodo letivo selecionado.
            # Caso não esteja, não retornara nenhuma nota dos alunos
            if school_year_date_info.get('init_date') > date.today():
                return ResponseHelper.HTTP_200({'results': {
                    'editable': False,
                    'term_grade': school_year_date_info.get('grade'),
                    'skill': school_year_date_info.get('skill'),
                    'grades': [],
                }})


            students_class, error = BSC.list_student_class(class_id)
            if error:
                return error
            # ids dos usuarios da turma
            user_ids = [student.get('fk_student_user')
                        for student in students_class]

            # verifica se a data atual corresponde ao termo escolhido
            # Caso não seja do termo, pode apenas visualizar as notas enteriores, mas não editar
            editable = is_current_term = validate_term_date(school_year_date_info)

            grades = []
            grades = BSG.get_students_grade(
                pedagogical_setting_data.get('fk_subject'), class_id, term)

            _ = [user_ids.remove(grade_item.get('fk_student_user')) for
                 grade_item in grades if grade_item.get('fk_student_user') in user_ids]

            # if is_current_term:
            for studet in user_ids:
                if is_current_term:
                    student_grade = BSG.build_student_grade_data(
                        user_id=studet,
                        class_id=class_id,
                        term_id=term,
                        subject_id=pedagogical_setting_data.get('fk_subject'))

                    student_grade_created, create_error = BSG.create_student_grade(
                        student_grade)
                    if create_error:
                        return create_error

                    grades.append(student_grade_created)

            logger.info('Retornando nota dos alunos.')
            return ResponseHelper.HTTP_200({
                'editable': editable,
                'term_grade': school_year_date_info.get('grade'),
                'skill': class_setting_obj.skill,
                'grades': grades
            })

        except Exception as error:
            message = 'Problemas ao visualizar SubjectGrade'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(TEACHER), name='dispatch')
class UpdateSubjectGradeView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, class_id, pedagogical_id, format=None) -> ResponseHelper:
        try:
            data = request.data
            term = int(request.GET.get("term", '1'))
            grades = data.get("grades", [])

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

            _ = [grades.remove(student_grade) for student_grade in deepcopy(grades)
                 if student_grade.get("fk_student_user") not in user_ids]

            if editable and is_current_term and grades:
                for grade in grades:
                    error = valeidate_sum_grades(grade, term_grade)
                    if error:
                        return error

                    SubjectGrade.objects.filter(
                        pk_subject_grade=grade.get("pk_subject_grade"),
                        fk_class = class_id,
                        fk_term = term,
                        fk_subject = pedagogical_setting_data.get('fk_subject'),
                        fk_student_user = grade.get('fk_student_user')
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
            message = 'Problemas ao editar SubjectGrade'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

