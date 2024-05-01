#!/usr/bin/python
# -*- encoding: utf-8 -*-

from rest_framework import status
from rest_framework.response import Response


class ResponseHelper:

    @staticmethod
    def HTTP_200 (data=None):
        """ HTTP_200_OK """
        return Response(data, status=status.HTTP_200_OK)
    
    @staticmethod
    def HTTP_201 (data=None):
        """ HTTP_201_CREATED """
        return Response(data, status=status.HTTP_201_CREATED)
    
    @staticmethod
    def HTTP_204 (data=None):
        """ HTTP_204_NO_CONTENT """
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    
    @staticmethod
    def HTTP_400 (data=None):
        """ HTTP_400_BAD_REQUEST """
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def HTTP_401 (data=None):
        """ HTTP_401_UNAUTHORIZED """
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod
    def HTTP_403 (data=None):
        """ HTTP_403_FORBIDDEN """
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def HTTP_404 (data=None):
        """ HTTP_404_NOT_FOUND """
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def HTTP_500 (data=None):
        """ HTTP_500_INTERNAL_SERVER_ERROR """
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)