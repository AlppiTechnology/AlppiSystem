#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from apps.academic.subject_area import view as subject_area_view
from apps.academic.subject import view as subject_view
from apps.academic.school_level import view as school_level_view
from apps.academic.shift import view as shift_view
from apps.academic.skill_settings import view as skill_settings_view
from apps.academic.school_grade import view as school_grade_view
from apps.academic.term import view as term_view
from apps.academic.term_type import view as term_type_view
from apps.academic.term_type import view as term_type_view
from apps.academic.school_year import view as school_year_view
from apps.academic.class_setting import view as class_setting_view
from apps.academic.pedagogical_setting import view as pedagogical_view
from apps.academic.subject_grade import views as subject_grade_view
from apps.academic.skill_grade import views as skill_grade_view
from apps.academic.student_presence import views as student_presence_view



urlpatterns = [
    # ------------- Subject Area / Area da Disciplina -------------
    path('subjectarea/<int:pk>/', subject_area_view.SubjectAreaView.as_view(), name='subject_area_data'),
    path('subjectarea/list/', subject_area_view.ListSubjectAreaView.as_view(), name='list_subject_area'),
    path('subjectarea/create/', subject_area_view.CreateSubjectAreaView.as_view(), name='create_subject_area'),
    path('subjectarea/<int:pk>/update/', subject_area_view.UpdateSubjectAreaView.as_view(), name='update_subject_area'),
    path('subjectarea/<int:pk>/delete/', subject_area_view.DeleteSubjectAreaView.as_view(), name='delete_subject_area'),
    path('subjectarea/<int:pk>/changestatus/', subject_area_view.ChangeStatusSubjectAreaView.as_view(), name='changestatus_subject_area'),

    # ------------- Subject / Disciplina -------------
    path('subject/<int:pk>/', subject_view.SubjectView.as_view(), name='subject_data'),
    path('subject/list/', subject_view.ListSubjectView.as_view(), name='list_subject'),
    path('subject/create/', subject_view.CreateSubjectView.as_view(), name='create_subject'),
    path('subject/<int:pk>/update/', subject_view.UpdateSubjectView.as_view(), name='update_subject'),
    path('subject/<int:pk>/delete/', subject_view.DeleteSubjectView.as_view(), name='delete_subject'),
    path('subject/<int:pk>/changestatus/', subject_view.ChangeStatusSubjectView.as_view(), name='changestatus_subject'),

    # ------------- Skill Settings / Configuracoes de Habilidades  -------------
    path('skillsettings/<int:pk>/', skill_settings_view.SkillSettingsView.as_view(), name='skill_settings_data'),
    path('skillsettings/list/', skill_settings_view.ListSkillSettingsView.as_view(), name='list_skill_settings'),
    path('skillsettings/create/', skill_settings_view.CreateSkillSettingsView.as_view(), name='create_skill_settings'),
    path('skillsettings/<int:pk>/update/', skill_settings_view.UpdateSkillSettingsView.as_view(), name='update_skill_settings'),
    path('skillsettings/<int:pk>/delete/', skill_settings_view.DeleteSkillSettingsView.as_view(), name='delete_skill_settings'),
    path('skillsettings/<int:pk>/changestatus/', skill_settings_view.ChangeStatusSkillSettingsView.as_view(), name='changestatus_skill_settings'),


    # ------------- School Level / Serie -------------
    path('schoollevel/list/', school_level_view.ListSchoolLevelView.as_view(), name='list_all_school_level'),
    path('schoollevel/<int:pk>/', school_level_view.SchoolLevelView.as_view(), name='get_school_level'),
    path('schoollevel/create/', school_level_view.CreateSchoolLevelView.as_view(), name='create_school_level'),
    path('schoollevel/<int:pk>/update/', school_level_view.UpdateSchoolLevelView.as_view(), name='update_school_level'),
    path('schoollevel/<int:pk>/delete/', school_level_view.DeleteSchoolLevelView.as_view(), name='delete_school_level'),

    # ------------- School Grade / Grau -------------
    path('schoolgrade/list/', school_grade_view.ListSchoolGradeView.as_view(), name='list_all_school_grade'),
    path('schoolgrade/<int:pk>/', school_grade_view.SchoolGradeView.as_view(), name='get_school_grade'),
    path('schoolgrade/create/', school_grade_view.CreateSchoolGradeView.as_view(), name='create_school_grade'),
    path('schoolgrade/<int:pk>/update/', school_grade_view.UpdateSchoolGradeView.as_view(), name='update_school_grade'),
    path('schoolgrade/<int:pk>/delete/', school_grade_view.DeleteSchoolGradeView.as_view(), name='delete_school_grade'),

    # ------------- Shift / Turno -------------
    path('shift/list/', shift_view.ListShiftView.as_view(), name='list_all_shift'),

    # ------------- Term / Etapas -------------
    path('term/list/', term_view.ListTermView.as_view(), name='list_all_term'),
    path('term/<int:pk>/', term_view.TermView.as_view(), name='get_term'),
    path('term/create/', term_view.CreateTermView.as_view(), name='create_term'),
    path('term/<int:pk>/update/', term_view.UpdateTermView.as_view(), name='update_term'),
    path('term/<int:pk>/delete/', term_view.DeleteTermView.as_view(), name='delete_term'),

    # ------------- Term Type / Tipo de Etapas -------------
    path('termtype/list/', term_type_view.ListTermTypeView.as_view(), name='list_all_term_type'),
    path('termtype/<int:pk>/', term_type_view.TermTypeView.as_view(), name='get_term_type'),
    path('termtype/create/', term_type_view.CreateTermTypeView.as_view(), name='create_term_type'),
    path('termtype/<int:pk>/update/', term_type_view.UpdateTermTypeView.as_view(), name='update_term_type'),
    path('termtype/<int:pk>/delete/', term_type_view.DeleteTermTypeView.as_view(), name='delete_term_type'),

    # ------------- Skill Settings / Configuracoes de Habilidades  -------------
    path('schoolyear/<int:pk>/', school_year_view.SchoolYearView.as_view(), name='school_year'),
    path('schoolyear/list/', school_year_view.ListSchoolYearView.as_view(), name='list_school_year'),
    path('schoolyear/create/', school_year_view.CreateSchoolYearView.as_view(), name='create_school_year'),
    path('schoolyear/<int:pk>/update/', school_year_view.UpdateSchoolYearView.as_view(), name='update_school_year'),
    path('schoolyear/<int:pk>/delete/', school_year_view.DeleteSchoolYearView.as_view(), name='delete_school_year'),
    path('schoolyear/<int:pk>/changestatus/', school_year_view.ChangeStatusSchoolYearView.as_view(), name='changestatus_school_year'),

    # ------------- Class Setting / Configuração de Turma  -------------
    path('class/<int:pk>/', class_setting_view.ClassSettingView.as_view(), name='class'),
    path('class/list/', class_setting_view.ListClassSettingView.as_view(), name='list_class'),
    path('class/create/', class_setting_view.CreateClassSettingView.as_view(), name='create_class'),
    path('class/<int:pk>/update/', class_setting_view.UpdateClassSettingView.as_view(), name='update_class'),
    path('class/<int:pk>/delete/', class_setting_view.DeleteClassSettingView.as_view(), name='delete_class'),
    path('class/<int:pk>/changestatus/', class_setting_view.ChangeStatusClassSettingView.as_view(), name='changestatus_class'),

    # ------------- Pedagogical Setting / Configuração de Pedagogica  -------------
    path('pedagogical/', pedagogical_view.ListPedagogicalView.as_view(), name='list_pedagogical'),

    # ------------- Subject Grade / Notas de Discilpinas -------------
    path('subjectgrade/<int:class_id>/<int:pedagogical_id>/', subject_grade_view.SubjectGradeView.as_view(), name='subject_grade'),
    path('subjectgrade/<int:class_id>/<int:pedagogical_id>/<int:term_id>/update/', subject_grade_view.UpdateSubjectGradeView.as_view(), name='subject_grade_update'),

    # ------------- Subject Grade / Notas de Discilpinas -------------
    path('skillgrade/<int:class_id>/<int:pedagogical_id>/<int:skill_id>/', skill_grade_view.SkillGradeView.as_view(), name='skill_grade'),
    path('skillgrade/<int:class_id>/<int:pedagogical_id>/<int:term_id>/<int:skill_id>/update/', skill_grade_view.UpdateSkillGradeView.as_view(), name='skill_grade_update'),

   # ------------- Subject Grade / Notas de Discilpinas -------------
    path('studentpresence/<int:class_id>/<int:pedagogical_id>/', student_presence_view.StudentPresenceView.as_view(), name='student_presence'),
    path('studentpresence/<int:class_id>/<int:pedagogical_id>/update/', student_presence_view.UpdateStudentPresenceView.as_view(), name='student_presence_update'),

]

urlpatterns = format_suffix_patterns(urlpatterns)