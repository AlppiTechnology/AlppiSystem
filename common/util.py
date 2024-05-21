#!/usr/bin/python
# -*- encoding: utf-8 -*-
from rest_framework import status
from django.http import JsonResponse
from datetime import datetime, date, timedelta

import logging



logger = logging.getLogger('django')


def get_ip_from_request(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META.get('REMOTE_ADDR')

def convert_date( date_to_format):
    return date.fromisoformat(date_to_format)

def convert_datetime( date, format='%Y-%m-%dT%H:%M:%S'):
    return datetime.strptime(date, format)


def uppercase_first(data:dict, items:list) -> None:
    '''
    Coloca a primeira letra das palavras de uma frase em MAIUSCOLA.\n
    
    Params:
        - data (dict): dict com as informações.\n
        - items (list): valores a serem modificados.
    '''
    prepositions = ['de', 'da', 'do', 'das', 'dos']

    for key, value in data.items():
        if key in items:
            name = value.split()
            formated_name = [palavra.title() if palavra.lower() not in prepositions else palavra.lower() for palavra in name]
            data[key] = ' '.join(formated_name)