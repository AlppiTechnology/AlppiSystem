#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import DRCTChapter
from apps.ct_requests.drct_chapter.serializer import DRCTChapterSerializer


logger = logging.getLogger('django')


class BaseDRCTChapter():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTChapter.objects.get(pk=pk), None)
        except DRCTChapter.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTChapter.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTChapter.objects.all(), None)
        except DRCTChapter.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTChapter.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_chapter_data(self, pk) -> tuple:
        """
            Captura os id da drct_chapter e dados serializados de um drct_chapter especifica
        """
        logger.info(f'Capturando dados do drct_chapter id:{pk}')
        drct_chapter_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTChapterSerializer(drct_chapter_id)
        return drct_chapter_id, selrializer.data
