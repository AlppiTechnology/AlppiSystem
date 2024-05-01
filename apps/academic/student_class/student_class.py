#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from datetime import datetime
from django.db.models import Q, F


from alppi.responses import ResponseHelper
from apps.academic.models import StudentClass
from apps.academic.student_class.serializer import StudentClassSerializer
from apps.academic.student_class.validations import validate_repeated_student, validate_students_update


logger = logging.getLogger('django')


class BaseStudentClass():

    def get_object(self, pk) -> tuple:
        try:
            return (StudentClass.objects.get(pk=pk), None)
        except StudentClass.DoesNotExist:
            message = 'Não foi possivel encontrar este StudentClass.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (StudentClass.objects.all(), None)
        except StudentClass.DoesNotExist:
            message = 'Não foi possivel encontrar todos os StudentClass.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_student_class_data(self, pk) -> tuple:
        """
            Captura os id da student_class e dados serializados de um student_class especifica
        """
        logger.info(f'Capturando dados do student_class id:{pk}')
        student_class_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = StudentClassSerializer(student_class_id)
        return student_class_id, selrializer.data

    def list_student_class(self, fk_class_setting:int):
        
        try:
            student_class_obj = StudentClass.objects.annotate(
                student_name=F('fk_student_user__username')
            ).filter(
                fk_class_setting=fk_class_setting,
                status = True
            ).values('pk_student_class','fk_student_user','student_name','status'
            ).order_by('student_name')
            
            if student_class_obj:
                return list(student_class_obj), None
            
            return [], None

        except Exception as error:
            message = 'Problemas ao listar StudentClass'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def create_student_class(self, students:dict, fk_class_setting:int):
        try:
             # verifica se existe disciplinas repetidas
            repeated_student = validate_repeated_student(students)
            if repeated_student:
                return None, repeated_student
            
            for student_id in students:
                data = {}
                data['fk_class_setting'] = fk_class_setting
                data['fk_student_user'] = student_id
                data['status'] = 1

                serializer = StudentClassSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                else:
                    return  (None, ResponseHelper.HTTP_404({'detail': serializer.errors}))
            return None, None

        except StudentClass.DoesNotExist:
            message = 'Não foi possivel encontrar todos os StudentClass.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def update_student_class(self, students:dict, fk_class_setting:int):
        student_old = StudentClass.objects.annotate(
            ).filter(
                fk_class_setting=fk_class_setting,
                status=True
            ).values('pk_student_class','fk_student_user')
        
        if student_old:
            student_old = list(student_old)

        else: 
            student_old = []

        to_delete, to_add = validate_students_update(student_old, students)

        # Não pode deletar pois existe a relação entre as tabelas, então
        # somente e desativado.
        for student_class_delete in to_delete:

            student_class_obj , error = self.get_object(student_class_delete)
            if error:
                return None, error
            
            student_class_obj.status = False
            student_class_obj.save()

        # Adiciona novos estudantes a turma
        if to_add:
            _, error = self.create_student_class(to_add, fk_class_setting)
            if error:
                    return None, error
                

        return None, None

    def delete_student_class(self, fk_class_setting:int):
        try:
            student_class_obj = StudentClass.objects.filter(
                fk_class_setting=fk_class_setting)

            student_class_obj.delete()

            return None, None
        
        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
        
    def change_status_all_student_classg(self, fk_class_setting:int, changed_status:int):
        try:
            student_class_objs = StudentClass.objects.filter(
                fk_class_setting=fk_class_setting)

            for student_class_obj in student_class_objs:
                student_class_obj.status = changed_status
                student_class_obj.save()

            return None, None
        
        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})