#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import DRCTComment
from apps.ct_requests.drct_comment.serializer import DRCTCommentSerializer


logger = logging.getLogger('django')


class BaseDRCTComment():

    def get_object(self, pk) -> tuple:
        try:
            return (DRCTComment.objects.get(pk=pk), None)
        except DRCTComment.DoesNotExist:
            message = 'Não foi possivel encontrar este DRCTComment.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (DRCTComment.objects.all(), None)
        except DRCTComment.DoesNotExist:
            message = 'Não foi possivel encontrar todos os DRCTComment.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_drct_comment_data(self, pk) -> tuple:
        """
            Captura os id da drct_comment e dados serializados de um drct_comment especifica
        """
        logger.info(f'Capturando dados do drct_comment id:{pk}')
        drct_comment_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = DRCTCommentSerializer(drct_comment_id)
        return drct_comment_id, selrializer.data
