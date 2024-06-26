#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from apps.ct_requests.drct_regulament import view as regulament_view
from apps.ct_requests.drct_internal_note import view as internal_note_view
from apps.ct_requests.drct_student_internal_note import view as student_internal_note_view
from apps.ct_requests.drct_comment import view as comment_view



urlpatterns = [
    # ------------- regulament / Regulamentos -------------
    path('regulament/list/', regulament_view.ListDRCTRegulamentView.as_view(), name='regulament_list'),
    path('regulament/create/', regulament_view.CreateDRCTRegulamentView.as_view(), name='regulament_create'),
    path('regulament/<int:pk>/', regulament_view.DRCTRegulamentView.as_view(), name='regulament_data'),
    path('regulament/<int:pk>/update/', regulament_view.UpdateDRCTRegulamentView.as_view(), name='regulament_update'),
    path('regulament/<int:pk>/delete/', regulament_view.DeleteDRCTRegulamentView.as_view(), name='regulament_delete'),

    # ------------- DRCTInternalNote / Comunicado Interno (CI) -------------
    path('internal_note/list/', internal_note_view.ListDRCTInternalNoteView.as_view(), name='internal_note_list'),
    path('internal_note/create/', internal_note_view.CreateDRCTInternalNoteView.as_view(), name='internal_note_create'),
    path('internal_note/<int:pk>/', internal_note_view.DRCTInternalNoteView.as_view(), name='internal_note_data'),
    path('internal_note/<int:pk>/update/', internal_note_view.UpdateDRCTInternalNoteView.as_view(), name='internal_note_update'),
    path('internal_note/<int:pk>/delete/', internal_note_view.DeleteDRCTInternalNoteView.as_view(), name='internal_note_delete'),

    # ------------- DRCTStudentInternalNote / Estudante do Comunicado Interno -------------
    path('student_internal_note/list/', student_internal_note_view.ListDRCTStudentInternalNoteView.as_view(), name='student_internal_note_list'),
    path('student_internal_note/create/', student_internal_note_view.CreateDRCTStudentInternalNoteView.as_view(), name='student_internal_note_create'),
    path('student_internal_note/<int:pk>/', student_internal_note_view.DRCTStudentInternalNoteView.as_view(), name='student_internal_note_data'),
    path('student_internal_note/<int:pk>/update/', student_internal_note_view.UpdateDRCTStudentInternalNoteView.as_view(), name='student_internal_note_update'),
    path('student_internal_note/<int:pk>/delete/', student_internal_note_view.DeleteDRCTStudentInternalNoteView.as_view(), name='student_internal_note_delete'),


    # ------------- Comment / Comentarios -------------
    path('comment/list/', comment_view.ListDRCTCommentView.as_view(), name='comment_list'),
    path('comment/create/', comment_view.CreateDRCTCommentView.as_view(), name='comment_create'),
    path('comment/<int:pk>/', comment_view.DRCTCommentView.as_view(), name='comment_data'),
    path('comment/<int:pk>/update/', comment_view.UpdateDRCTCommentView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', comment_view.DeleteDRCTCommentView.as_view(), name='comment_delete'),


]

urlpatterns = format_suffix_patterns(urlpatterns)