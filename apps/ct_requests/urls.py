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

]

urlpatterns = format_suffix_patterns(urlpatterns)