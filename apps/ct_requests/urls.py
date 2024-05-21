#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from apps.ct_requests.drct_chapter import view as chapter_view
from apps.ct_requests.drct_section import view as section_view
from apps.ct_requests.drct_paragraph import view as paragraph_view
from apps.ct_requests.drct_penalty import view as penalty_view
from apps.ct_requests.drct_severity import view as severity_view
from apps.ct_requests.drct_request import view as request_view
from apps.ct_requests.drct_student_request import view as student_request_view
from apps.ct_requests.drct_comment import view as comment_view



urlpatterns = [
    # ------------- Chapter / Captulo -------------
    path('chapter/list/', chapter_view.ListDRCTChapterView.as_view(), name='chapter_list'),
    path('chapter/create/', chapter_view.CreateDRCTChapterView.as_view(), name='chapter_create'),
    path('chapter/<int:pk>/', chapter_view.DRCTChapterView.as_view(), name='chapter_data'),
    path('chapter/<int:pk>/update/', chapter_view.UpdateDRCTChapterView.as_view(), name='chapter_update'),
    path('chapter/<int:pk>/delete/', chapter_view.DeleteDRCTChapterView.as_view(), name='chapter_delete'),

    # ------------- Section / Artigo -------------
    path('section/list/', section_view.ListDRCTSectionView.as_view(), name='section_list'),
    path('section/create/', section_view.CreateDRCTSectionView.as_view(), name='section_create'),
    path('section/<int:pk>/', section_view.DRCTSectionView.as_view(), name='section_data'),
    path('section/<int:pk>/update/', section_view.UpdateDRCTSectionView.as_view(), name='section_update'),
    path('section/<int:pk>/delete/', section_view.DeleteDRCTSectionView.as_view(), name='section_delete'),

    # ------------- Paragraph / Paragrafo -------------
    path('paragraph/list/', paragraph_view.ListDRCTParagraphView.as_view(), name='paragraph_list'),
    path('paragraph/create/', paragraph_view.CreateDRCTParagraphView.as_view(), name='paragraph_create'),
    path('paragraph/<int:pk>/', paragraph_view.DRCTParagraphView.as_view(), name='paragraph_data'),
    path('paragraph/<int:pk>/update/', paragraph_view.UpdateDRCTParagraphView.as_view(), name='paragraph_update'),
    path('paragraph/<int:pk>/delete/', paragraph_view.DeleteDRCTParagraphView.as_view(), name='paragraph_delete'),

    # ------------- Severity / Criticidade -------------
    path('severity/list/', severity_view.ListDRCTSeverityView.as_view(), name='severity_list'),
    path('severity/create/', severity_view.CreateDRCTSeverityView.as_view(), name='severity_create'),
    path('severity/<int:pk>/', severity_view.DRCTSeverityView.as_view(), name='severity_data'),
    path('severity/<int:pk>/update/', severity_view.UpdateDRCTSeverityView.as_view(), name='severity_update'),
    path('severity/<int:pk>/delete/', severity_view.DeleteDRCTSeverityView.as_view(), name='severity_delete'),

    # ------------- Penalty / Penalidade -------------
    path('penalty/list/', penalty_view.ListDRCTPenaltyView.as_view(), name='penalty_list'),
    path('penalty/create/', penalty_view.CreateDRCTPenaltyView.as_view(), name='penalty_create'),
    path('penalty/<int:pk>/', penalty_view.DRCTPenaltyView.as_view(), name='penalty_data'),
    path('penalty/<int:pk>/update/', penalty_view.UpdateDRCTPenaltyView.as_view(), name='penalty_update'),
    path('penalty/<int:pk>/delete/', penalty_view.DeleteDRCTPenaltyView.as_view(), name='penalty_delete'),


]

urlpatterns = format_suffix_patterns(urlpatterns)