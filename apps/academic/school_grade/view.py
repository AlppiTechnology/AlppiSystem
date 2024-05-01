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
from apps.academic.school_grade.serializer import SchoolGradeSerializer
from apps.academic.models import SchoolGrade
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

@method_decorator(permission_required(SUPERUSER), name='dispatch')
class ListSchoolGradeView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed, HasPermission]

    def get(self, request, format=None) -> ResponseHelper:
        try:
            school_level = request.GET.get('level', None)

            if school_level:
                school_grade = SchoolGrade.objects.filter(fk_school_level=school_level)
            
            else:
                school_grade = SchoolGrade.objects.all()

            shift_paginate = self.paginate_queryset(
                school_grade, request, view=self)

            serializer = SchoolGradeSerializer(
                shift_paginate, many=True)
            return  ResponseHelper.HTTP_200(self.get_paginated_response(serializer.data).data)


        except Exception as error:
            message = 'Problemas ao listar todos os SchoolGrade.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'detail': message, 'error:': str(error)})
