#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging

from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from alppi.auth.authentication import JwtAutenticationAlppi
from alppi.auth.permissions import  IsViewAllowed
from alppi.responses import ResponseHelper
from alppi.utils.decorators import jwt_verifier
from apps.register.models import City
from apps.register.city.serializer import CitySerializer
from common.pagination.pagination import CustomPagination


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

  
class SerachCityView(APIView, CustomPagination):
    authentication_classes  = [JwtAutenticationAlppi]
    permission_classes = [IsViewAllowed]

    @method_decorator(jwt_verifier, name='dispatch')
    def get(self, request, format=None):
        try:

            city_name = request.GET.get('city_name',None)

            if city_name:
                city_list = City.objects.filter(city_name__startswith=city_name.title())
            else:
                return  ResponseHelper.HTTP_200({'results': []})

            serializer = CitySerializer(city_list, many=True)

            return  ResponseHelper.HTTP_200({'results': serializer.data})
 

        except Exception as error:
            message = 'Problemas ao listar todos os City.'
            logger.error({'results': message, 'error:': str(error)})
            return ResponseHelper.HTTP_500({'results': message, 'error:': str(error)})
