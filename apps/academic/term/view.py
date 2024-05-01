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
from apps.academic.term.serializer import TermSerializer
from apps.academic.models import Term
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListTermView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            
            term_type = request.GET.get('term_type', None)

            if term_type:
                terms = Term.objects.filter(fk_term_type=term_type)
            else:
                terms = Term.objects.all()

            term_paginate = self.paginate_queryset(
                terms, request, view=self)

            serializer = TermSerializer(
                term_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)


        except Exception as error:
            message = 'Problemas ao listar todos os Term.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
