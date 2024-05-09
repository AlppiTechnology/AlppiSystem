#!/usr/bin/python
# -*- encoding: utf-8 -*-
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from alppi.responses import ResponseHelper

TERM_TYPE = {
    1 : (1,2,3,4),
    2 : (5,6,7),
    3 : (8,9)
}

def validate_terms(dates, term_type) -> bool:
    term_type_allowed = TERM_TYPE.get(int(term_type))
    for date in dates:
        if date.get('fk_term') not in term_type_allowed:
            return ResponseHelper.HTTP_400({'detail':'Etapa não corresponsdente ao Tipo de Etapa'})
        
    if len(dates) != len(term_type_allowed):
        return ResponseHelper.HTTP_400({'detail':f'É nescessário ter data para {len(term_type_allowed)} termos.'})


def validate_dates(dates) -> bool:
    last_final_date = None

    for date_item in dates:
        init_date = date.fromisoformat(date_item.get('init_date'))
        final_date = date.fromisoformat(date_item.get('final_date'))

        if init_date >= final_date:
            return ResponseHelper.HTTP_400({'detail':f'A data {init_date} Precisa ser maior que a {final_date}'})
        
        if last_final_date and init_date < last_final_date:
            return ResponseHelper.HTTP_400({'detail':f'A data {init_date} Precisa ser maior que a {last_final_date}'})
        
        last_final_date = final_date

        date_item['init_date'] = init_date
        date_item['final_date'] = final_date
    

def validate_term_grade(data, total_grade):
    sum_grades = 0 
    
    for index in data:
        sum_grades += index.get('grade')

    if sum_grades != total_grade:
        return ResponseHelper.HTTP_400({'detail':f'A soma das etapas não totalizam {total_grade}'})
