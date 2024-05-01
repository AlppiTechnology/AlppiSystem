#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from django.db.models import Q, F

from alppi.responses import ResponseHelper
from apps.academic.models import SchoolYearSkill
from apps.academic.school_year_skill.serializer import SchoolYearSkillSerializer



logger = logging.getLogger('django')


class BaseSchoolYearSkill():

    def get_object(self, pk) -> tuple:
        try:
            return (SchoolYearSkill.objects.get(pk=pk), None)
        except SchoolYearSkill.DoesNotExist:
            message = 'Não foi possivel encontrar este SchoolYearSkill.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (SchoolYearSkill.objects.all(), None)
        except SchoolYearSkill.DoesNotExist:
            message = 'Não foi possivel encontrar todos os SchoolYearSkill.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_school_year_skill_data(self, pk) -> tuple:
        """
            Captura os id da school_year_skill e dados serializados de um school_year_skill especifica
        """
        logger.info(f'Capturando dados do school_year_skill id:{pk}')
        school_year_skill_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = SchoolYearSkillSerializer(school_year_skill_id)
        return school_year_skill_id, selrializer.data

    def list_school_year_skill(self, fk_school_year:int):
        
        try:
            school_year_date_skill = SchoolYearSkill.objects.annotate(
                label_name=F('fk_skill__label_name')
            ).filter(
                fk_school_year=fk_school_year
            ).values('pk_school_year_skill','fk_skill','label_name'
            ).order_by('label_name')
            
            if school_year_date_skill:
                return list(school_year_date_skill), None
            
            return [], None

        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def create_school_year_skill(self, skills_list:list, fk_school_year:int) -> tuple:

        try:
            saved_school_year_skill = []

            for pk_skill in skills_list:
                school_year_skill = {
                    'fk_skill':pk_skill,
                    'fk_school_year':fk_school_year
                }

                serializer = SchoolYearSkillSerializer(data=school_year_skill)
                if serializer.is_valid():
                    serializer.save()

                    saved_school_year_skill.append(serializer.data)

                else:
                    return None, ResponseHelper.HTTP_400({'detail': serializer.errors})
                
            return saved_school_year_skill, None

        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearSkill'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def delete_school_year_skill(self, fk_school_year:int):
        try:
            school_year_skill_obj = SchoolYearSkill.objects.filter(
                fk_school_year=fk_school_year)

            school_year_skill_obj.delete()

            return None, None
        
        except Exception as error:
            message = 'Problemas ao cadastrar SchoolYearDate'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})

    def update_school_year_skill(self,  skills_list:list, fk_school_year:int) -> tuple:
        try:
            school_year_skill = SchoolYearSkill.objects.filter(
                fk_school_year=fk_school_year
            ).values('pk_school_year_skill', 'fk_skill')

            school_year_skill = {item['fk_skill']:item['pk_school_year_skill'] for item in school_year_skill}
            
            # Ids do valores já existentes
            skills_list_data = set(school_year_skill.keys())
            
            # retirando ids duplicados
            skills_list = set(skills_list)

            skill_add = skills_list - skills_list_data
            skill_del = skills_list_data - skills_list

            delete_id = [school_year_skill[skill_id] for skill_id in skill_del]

            if delete_id:
                error = self.delete_school_year_skill(delete_id)

            if skill_add:
                _, error = self.create_school_year_skill(
                skill_add, fk_school_year)

                if error:
                    return None, error

            return None, None

        except Exception as error:
            message = 'Problemas ao atualizar SchoolYearSkill'
            logger.error({'results': message, 'error:': str(error)})
            return None, ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
