#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from alppi.responses import ResponseHelper
from apps.ct_requests.models import CTCIComment
from apps.ct_requests.ct_ci_comment.serializer import CTCICommentSerializer


logger = logging.getLogger('django')


class BaseCTCIComment():

    def get_object(self, pk) -> tuple:
        try:
            return (CTCIComment.objects.get(pk=pk), None)
        except CTCIComment.DoesNotExist:
            message = 'Não foi possivel encontrar este CTCIComment.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_all_object(self) -> tuple:
        try:
            return (CTCIComment.objects.all(), None)
        except CTCIComment.DoesNotExist:
            message = 'Não foi possivel encontrar todos os CTCIComment.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))

    def get_ct_ci_comment_data(self, pk) -> tuple:
        """
            Captura os id da ct_ci_comment e dados serializados de um ct_ci_comment especifica
        """
        logger.info(f'Capturando dados do ct_ci_comment id:{pk}')
        ct_ci_comment_id, has_error = self.get_object(pk=pk)
        if has_error:
            return None, has_error

        selrializer = CTCICommentSerializer(ct_ci_comment_id)
        return ct_ci_comment_id, selrializer.data

    def create_pct_ci_comment(self, internal_note:int, comment:str, user_id:int):
        try:

            data = {}
            data['fk_ct_ci_internal_note'] = internal_note
            data['fk_user'] = user_id
            data['comment'] = comment

            serializer = CTCICommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return None, None

            else:
                return  (None, ResponseHelper.HTTP_404({'detail': serializer.errors}))

        except CTCIComment.DoesNotExist:
            message = 'Não foi possivel encontrar todos os CTCIComment.'
            logger.error({'results': message})
            return  (None, ResponseHelper.HTTP_404({'detail': message}))
