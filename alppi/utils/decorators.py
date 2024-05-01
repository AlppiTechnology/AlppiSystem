#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
import jwt


from functools import wraps
from rest_framework import status
from alppi.jwt.jwt_encrypt import decrypt_jwt_pass
from django.http import JsonResponse

from common.systemModules.system_modules import SystemModules



logger = logging.getLogger('django')



def jwt_verifier(function):
    """
    Decorador para verificar Tokens JSON Web (JWT) em views do Django.

    Este decorador extrai o JWT do cabeçalho 'Authorization' na solicitação HTTP,
    decodifica e verifica o token e anexa a carga útil decodificada ao objeto de solicitação
    para processamento adicional na view decorada.

    Args:
        funcao (callable): A função de visualização a ser decorada.

    Returns:
        callable: A função de visualização decorada.

    Raises:
        JsonResponse: Retorna uma resposta JSON com uma mensagem de erro se a verificação do token falhar.

    """
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        AUTHORIZATION = request.headers.get('Authorization')

        if not AUTHORIZATION:
            message = 'Sem Token. Bad Request'
            logger.error({'results': message})
            return JsonResponse({
                'results': message
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            jwt_token = AUTHORIZATION.split()
            jwt_token_decoded = decrypt_jwt_pass(jwt_token[1])
            request.jwt_token = jwt_token_decoded

            return function(request=request, *args, **kwargs)

        except jwt.ExpiredSignatureError as error:
            message = 'Token expirado!'
            logger.error({'results': message})
            logger.error(error)
            return JsonResponse({
                'results': message
            }, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.InvalidSignatureError as error:
            message = 'Token invalido!'
            logger.error({'results': message})
            logger.error(error)
            return JsonResponse({
                'results': 'Token invalido'
            }, status=status.HTTP_401_UNAUTHORIZED)

        except KeyError as error:
            message = 'Token invalido!'
            logger.error({'results': message})
            logger.error(error)
            return JsonResponse({
                'results': 'Token invalido'
            }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as error:
            message = 'Token inesperado.'
            logger.error({'results': message})
            logger.error(error)
            return JsonResponse({
                'results': message
            }, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper

def load_system_modules(function):
    """
    Decorador para carregar informações dos módulos disponíveis no sistema e adicioná-los à requisição.

    Este decorador cria uma instância de `SystemModules`, obtém os módulos disponíveis e decodifica
    as informações. Em seguida, adiciona os módulos à requisição antes de chamar a função original.

    Parâmetros:
    - function: A função original que será decorada.

    Retorna:
    function: Uma função decorada que carrega os módulos do sistema antes de chamar a função original.

    Exceções:
    - JsonResponse: Retorna uma resposta JSON com uma mensagem de erro e status HTTP 500
      em caso de problemas ao carregar informações dos módulos disponíveis do sistema.

    """

    @wraps(function)
    def wrapper(request, *args, **kwargs):
        try:
            SM = SystemModules()
            SM.get_modules()
            system_modules = SM.decoded_system_modules()

            request.system_modules = system_modules

            return function(request=request, *args, **kwargs)
        except Exception as error:
            message = 'Problemas ao carregar informações dos modulos disponiveis do sistema.'
            logger.error({'results': message})
            logger.error(error)
            return JsonResponse({
                'results': message
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return function(request=request, *args, **kwargs)
    return wrapper

def permission_model_required(model=None):
    """
    Decorador para adicionar o modelo (model) à requisição como parte da verificação de permissão.

    Este decorador adiciona o modelo fornecido à requisição antes de chamar a função original.
    O modelo pode ser utilizado posteriormente para verificar permissões específicas na função decorada.

    Parâmetros:
    - model (str): O nome do modelo (opcional). Se não fornecido, o valor padrão é None.

    Retorna:
    function: Uma função decorada que adiciona o modelo à requisição.
    """
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
        
            request.model_perm = model.lower()

            return function(request=request, *args, **kwargs)
        return wrapper
    return decorator

def permission_required(permission=None):
    """
    Decorador para adicionar a permissão necessária à requisição como parte da verificação de permissão.

    Este decorador adiciona a permissão fornecida à requisição antes de chamar a função original.
    A permissão pode ser utilizada posteriormente para verificar permissões específicas na função decorada.

    Parâmetros:
    - permission (str): A permissão necessária (opcional). Se não fornecido, o valor padrão é None.

    Retorna:
    function: Uma função decorada que adiciona a permissão à requisição.
    """
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):

            request.permission_required = permission

            return function(request=request, *args, **kwargs)
        return wrapper
    return decorator