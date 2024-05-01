#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
import os

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from alppi.utils.groups import GROUPS
from apps.register.models import User



logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

class HasPermission(BasePermission):
    """
    Permissão personalizada para verificar se um usuário tem as permissões necessárias para acessar uma rota.

    Esta classe estende a classe BasePermission do Django REST Framework e implementa a lógica para verificar
    se um usuário possui as permissões necessárias com base nas informações da requisição.

    Métodos:
    - has_permission(request, view): Verifica se o usuário tem as permissões necessárias.

    Atributos:
    - method_permissions: Mapeamento de métodos HTTP para permissões específicas.

    Exceções:
    - PermissionDenied: Lançada se o usuário não tiver as permissões necessárias.

    """

    def has_permission(self, request, view):
        """
        Verifica se o usuário tem as permissões necessárias.

        Parâmetros:
        - request: A instância da requisição Django.
        - view: A instância da view Django.

        Retorna:
        bool: True se o usuário tiver as permissões necessárias, False caso contrário.

        Exceções:
        - PermissionDenied: Lançada se o usuário não tiver as permissões necessárias.
        """
        get_user(request)
        permission_required, level_required = request.permission_required
        # Mapear métodos para permissões específicas (ajuste conforme necessário)
        method_permissions = {
            'GET': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete'
        }

        # Obter a permissão necessária com base no método da requisição
        required_permission = method_permissions.get(request.method, None)
        
        # permissão de deleção somente para usuarios ALPPI
        if required_permission.startswith('delete') and not request.user.is_superuser:
            return False

        if not required_permission:
            # Método não suportado, negar acesso
            return False
        
        # caso seja user usuario ou staff tem permissão total
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        # captura o nivel de acesso com a numeração
        if request.jwt_token.get('group'):
            group = request.jwt_token.get('group').lower()
            level_group = GROUPS.get(group)

        # Verificar as permissões na tabela auth_user_groups
        user_groups = request.user.groups.all()
        group_names = [group.name for group in user_groups]
        if permission_required in group_names and level_group in level_required:
            return True


        # Se nenhuma permissão foi encontrada, negar acesso
        # return False
        raise PermissionDenied("Este usuario não tem permissão para acessar esta rota.")


class IsViewAllowed(BasePermission):
    """
    Permissão personalizada para determinar se um usuário tem permissão para visualizar um objeto específico.

    Esta classe estende a classe BasePermission do Django REST Framework e implementa a lógica para determinar
    se um usuário tem permissão para visualizar um objeto específico. A decisão é baseada na função `get_user`,
    que verifica se o usuário associado ao token JWT pode ser obtido e adicionado à requisição.

    Métodos:
    - has_object_permission(request, view, obj): Verifica se o usuário tem permissão para visualizar o objeto.

    Exceções:
    - PermissionDenied: Lançada se o usuário não tiver permissão para visualizar o objeto.

    """
    def has_object_permission(self,request, view, obj) -> bool:

        """
        Verifica se o usuário tem permissão para visualizar o objeto.

        Parâmetros:
        - request: A instância da requisição Django.
        - view: A instância da view Django.
        - obj: O objeto a ser visualizado.

        Retorna:
        bool: True se o usuário tem permissão, False caso contrário.

        Exceções:
        - PermissionDenied: Lançada se o usuário não tiver permissão para visualizar o objeto.
        "
        """
        return get_user(request)


class IsAuthenticatedAlppi(BasePermission):
    """
    Permissão personalizada para verificar se um usuário possui as permissões adequadas na aplicação Alppi.

    Esta classe estende a classe BasePermission do Django REST Framework e implementa a lógica para verificar
    se um usuário autenticado possui as permissões necessárias para acessar uma determinada rota na aplicação Alppi.

    Métodos:
    - has_permission(request, view): Verifica se o usuário possui as permissões necessárias com base na requisição.
    - get_user(request): Obtém o usuário associado ao token JWT e o adiciona ao objeto de requisição.

    Atributos:
    - method_permissions: Mapeamento de métodos HTTP para permissões específicas.

    Exceções:
    - PermissionDenied: Lançada se o usuário não tiver as permissões necessárias.
    """

    def has_permission(self, request, view) -> bool:
        """
        Verifica se o usuário possui as permissões necessárias com base na requisição.

        Parâmetros:
        - request: A instância da requisição Django.
        - view: A instância da view Django.

        Retorna:
        bool: True se o usuário tiver as permissões necessárias, False caso contrário.

        Exceções:
        - PermissionDenied: Lançada se o usuário não tiver as permissões necessárias.

        """
        get_user(request)
        model = request.model_perm
        # Mapear métodos para permissões específicas (ajuste conforme necessário)
        method_permissions = {
            'GET': f'view_{model}',
            'POST': f'add_{model}',
            'PUT': f'change_{model}',
            'PATCH': f'change_{model}',
            'DELETE': f'delete_{model}'
        }

        # Obter a permissão necessária com base no método da requisição
        required_permission = method_permissions.get(request.method, None)
        
        # permissão de deleção somente para usuarios ALPPI
        if required_permission.startswith('delete_') and not request.user.is_superuser:
            return False

        if request.user.has_perm(required_permission):
            return True

        if not required_permission:
            # Método não suportado, negar acesso
            return False

        # Verificar as permissões na tabela auth_user_user_permissions
        user_permissions = request.user.user_permissions.all()
        if any(permission.codename == required_permission for permission in user_permissions):
            return True

        # Verificar as permissões na tabela auth_user_groups
        user_groups = request.user.groups.all()
        for group in user_groups:
            group_permissions = group.permissions.all()
            if any(permission.codename == required_permission for permission in group_permissions):
                return True

        # Se nenhuma permissão foi encontrada, negar acesso
        # return False
        raise PermissionDenied("Este usuario não tem permissão para acessar esta rota.")
    



def get_user( request) -> bool:
    """
    Obtém um usuário com base no número de registro presente no token JWT e o adiciona ao objeto de requisição.

    Esta função é utilizada para obter o usuário associado ao número de registro presente no token JWT,
    e adiciona o usuário ao objeto de requisição.

    Parâmetros:
    - request: A instância da requisição Django.

    Retorna:
    bool: True se o usuário foi encontrado e adicionado à requisição, False caso contrário.

    Exceções:
    - User.DoesNotExist: Lançada se o usuário não for encontrado no banco de dados.

    """
    try:
        registration = request.jwt_token.get('registration')
        user = User.objects.get(registration=registration)
        request.user  = user

        if not request.user.is_active:
            logger.error({'results': 'Usuario inativo.'})
            return False
        
        return True if user else False
    except User.DoesNotExist:
        message = 'Não foi possivel encontrar este User.'
        logger.error({'results': message})
        return False
