#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging

from datetime import datetime
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import HasPermission, IsViewAllowed
from alppi.responses import ResponseHelper
from alppi.utils.decorators import permission_required
from alppi.utils.groups import SUPERUSER
from apps.academic.term_type.serializer import TermTypeSerializer
from apps.academic.models import TermType
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListTermTypeView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            term_types = TermType.objects.all()
            term_type_paginate = self.paginate_queryset(
                term_types, request, view=self)

            serializer = TermTypeSerializer(
                term_type_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)


        except Exception as error:
            message = 'Problemas ao listar todos os TermType.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
