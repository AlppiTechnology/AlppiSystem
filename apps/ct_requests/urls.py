#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from apps.ct_requests.ct_ci_regulament import view as regulament_view
from apps.ct_requests.ct_ci_internal_note import view as internal_note_view
from apps.ct_requests.ct_ci_student_internal_note import view as student_internal_note_view
from apps.ct_requests.ct_ci_comment import view as comment_view



urlpatterns = [
    # ------------- regulament / Regulamentos -------------
    path('regulament/list/', regulament_view.ListCTCIRegulamentView.as_view(), name='regulament_list'),
    path('regulament/create/', regulament_view.CreateCTCIRegulamentView.as_view(), name='regulament_create'),
    path('regulament/<int:pk>/', regulament_view.CTCIRegulamentView.as_view(), name='regulament_data'),
    path('regulament/<int:pk>/update/', regulament_view.UpdateCTCIRegulamentView.as_view(), name='regulament_update'),
    path('regulament/<int:pk>/delete/', regulament_view.DeleteCTCIRegulamentView.as_view(), name='regulament_delete'),

    # ------------- CTCIInternalNote / Comunicado Interno (CI) -------------
    path('internal_note/list/', internal_note_view.ListCTCIInternalNoteView.as_view(), name='internal_note_list'),
    path('internal_note/create/', internal_note_view.CreateCTCIInternalNoteView.as_view(), name='internal_note_create'),
    path('internal_note/<int:pk>/', internal_note_view.CTCIInternalNoteView.as_view(), name='internal_note_data'),
    path('internal_note/<int:pk>/update/', internal_note_view.UpdateCTCIInternalNoteView.as_view(), name='internal_note_update'),
    path('internal_note/<int:pk>/delete/', internal_note_view.DeleteCTCIInternalNoteView.as_view(), name='internal_note_delete'),

    # ------------- CTCIStudentInternalNote / Estudante do Comunicado Interno -------------
    path('student_internal_note/list/', student_internal_note_view.ListCTCIStudentInternalNoteView.as_view(), name='student_internal_note_list'),
    path('student_internal_note/create/', student_internal_note_view.CreateCTCIStudentInternalNoteView.as_view(), name='student_internal_note_create'),
    path('student_internal_note/<int:pk>/', student_internal_note_view.CTCIStudentInternalNoteView.as_view(), name='student_internal_note_data'),
    path('student_internal_note/<int:pk>/update/', student_internal_note_view.UpdateCTCIStudentInternalNoteView.as_view(), name='student_internal_note_update'),
    path('student_internal_note/<int:pk>/delete/', student_internal_note_view.DeleteCTCIStudentInternalNoteView.as_view(), name='student_internal_note_delete'),


    # ------------- Comment / Comentarios -------------
    path('comment/list/', comment_view.ListCTCICommentView.as_view(), name='comment_list'),
    path('comment/create/', comment_view.CreateCTCICommentView.as_view(), name='comment_create'),
    path('comment/<int:pk>/', comment_view.CTCICommentView.as_view(), name='comment_data'),
    path('comment/<int:pk>/update/', comment_view.UpdateCTCICommentView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', comment_view.DeleteCTCICommentView.as_view(), name='comment_delete'),


]

urlpatterns = format_suffix_patterns(urlpatterns)