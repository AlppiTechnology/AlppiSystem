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
from apps.academic.models import SkillGrade
from apps.academic.pedagogical_setting.pedagogical_setting import BasePedagogicalSetting
from apps.academic.school_year_date.school_year_date import BaseSchoolYearDate
from apps.academic.student_class.student_class import BaseStudentClass
from apps.academic.skill_grade.serializer import SkillGradeSerializer
from apps.academic.skill_grade.skill_grade import BaseSkillGrade
from apps.academic.skill_grade.validations import valeidate_sum_grades, validate_employee_visualisation, validate_term_date
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')


@method_decorator(permission_required(TEACHER), name='dispatch')
class SkillGradeView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, class_id, pedagogical_id, skill_id, format=None) -> ResponseHelper:

        try:
            term = int(request.GET.get("term", '1'))
            BCS = BaseClassSetting()
            BPS = BasePedagogicalSetting()
            BSC = BaseStudentClass()
            BSYD = BaseSchoolYearDate()
            BSG = BaseSkillGrade()

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

            # Verifia se a data atual e menor que o inicio do periodo letivo selecionado.
            # Caso não esteja, não retornara nenhuma nota dos alunos

            if school_year_date_info.get('init_date') > date.today():
                return ResponseHelper.HTTP_200({'results': {
                    'editable': False,
                    'term_grade': school_year_date_info.get('grade'),
                    'skill': school_year_date_info.get('skill'),
                    'skill_grades': [],
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

            skill_grades = []
            skill_grades = BSG.get_students_skill_grade(
                pedagogical_setting_data.get('fk_subject'), skill_id, class_id, term)

            _ = [user_ids.remove(grade_item.get('fk_student_user')) for
                 grade_item in skill_grades if grade_item.get('fk_student_user') in user_ids]

            # if is_current_term:
            for studet in user_ids:
                if is_current_term:
                    student_skill_grade = BSG.build_student_skill_grade_data(
                        user_id=studet,
                        class_id=class_id,
                        term_id=term,
                        subject_id=pedagogical_setting_data.get('fk_subject'),
                        skill_id=skill_id)

                    student_skill_grade_created, create_error = BSG.create_student_skill_grade(
                        student_skill_grade)
                    if create_error:
                        return create_error

                    skill_grades.append(student_skill_grade_created)

            logger.info('Retornando nota dos alunos.')
            return ResponseHelper.HTTP_200({
                'editable': editable,
                'term_grade': school_year_date_info.get('grade'),
                'skill': class_setting_obj.skill,
                'skill_grades': skill_grades
            })

        except Exception as error:
            message = 'Problemas ao visualizar SkillGrade'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(TEACHER), name='dispatch')
class UpdateSkillGradeView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, class_id, pedagogical_id, skill_id, format=None) -> ResponseHelper:
        try:
            data = request.data
            term = int(request.GET.get("term", '1'))
            skill_grades = data.get("skill_grades", [])

            jwt_token = request.jwt_token
            user = request.user

            BCS = BaseClassSetting()
            BPS = BasePedagogicalSetting()
            BSC = BaseStudentClass()
            BSYD = BaseSchoolYearDate()
            BSG = BaseSkillGrade()

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

            _ = [skill_grades.remove(student_grade) for student_grade in deepcopy(skill_grades)
                 if student_grade.get("fk_student_user") not in user_ids]

            if editable and is_current_term and skill_grades:
                for skill_grade in skill_grades:
                    error = valeidate_sum_grades(skill_grade, term_grade)
                    if error:
                        return error

                    SkillGrade.objects.filter(
                        pk_skill_grade=skill_grade.get("pk_skill_grade")
                    ).update(
                        edited=datetime.now(),
                        grade_1=skill_grade.get('grade_1'),
                        grade_2=skill_grade.get('grade_2'),
                        grade_3=skill_grade.get('grade_3'),
                        grade_4=skill_grade.get('grade_4'),
                        grade_5=skill_grade.get('grade_5'),
                    )
                return ResponseHelper.HTTP_200({'results': 'Notas editadas com sucesso'})
            else:
                return ResponseHelper.HTTP_400({"detail": "Não é possivel editar as notas nesse momento."})

        except Exception as error:
            message = 'Problemas ao editar SkillGrade'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class DeleteSkillGradeView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def delete(self, request, pk, format=None) -> ResponseHelper:
        try:
            subject_grade_obj, error = self.get_object(pk)
            if error:
                return error

            subject_grade_obj.delete()
            return ResponseHelper.HTTP_204()

        except Exception as error:
            message = 'Problemas ao deletar SkillGrade'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListSkillGradeView(APIView, CustomPagination):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            subject_grades = SkillGrade.objects.all()
            subject_grade_paginate = self.paginate_queryset(
                subject_grades, request, view=self)

            serializer = SkillGradeSerializer(
                subject_grade_paginate, many=True)
            return ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)

        except Exception as error:
            message = 'Problemas ao listar todos os SkillGrade.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class CreateSkillGradeView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def post(self, request, format=None) -> ResponseHelper:
        try:
            data = request.data

            serializer = SkillGradeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return ResponseHelper.HTTP_201({'results': serializer.data})

            return ResponseHelper.HTTP_400({'detail': serializer.errors})

        except Exception as error:
            message = 'Problemas ao cadastrar SkillGrade'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})


@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ChangeStatusSkillGradeView(APIView):
    authentication_classes = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def put(self, request, pk, format=None) -> ResponseHelper:
        try:
            data = request.data
            subject_grade_obj, error = self.get_object(pk)
            if error:
                return error

            subject_grade_obj.is_active = data.get('is_active')
            subject_grade_obj.save()
            logger.info('Alterando status do subject_grade para {}.'.format(
                data.get('is_active')))

            message = 'SkillGrade atualizado com sucesso.'
            return ResponseHelper.HTTP_200({'results': message})

        except Exception as error:

            message = 'Problemas ao alterar status do subject_grade'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
