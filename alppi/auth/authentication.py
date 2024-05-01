
#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
import jwt

from django.utils.translation import gettext_lazy as _

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ( AuthenticationFailed,
        NotAuthenticated, PermissionDenied)

from alppi.jwt.jwt_encrypt import decrypt_jwt_pass




logger = logging.getLogger('django')

class JwtAutenticationAlppi(BaseAuthentication):
    """
    Autenticação JWT para a aplicação Alppi.

    Esta classe implementa a autenticação baseada em JWT (JSON Web Token) para a aplicação Alppi,
    utilizando BaseAuthentication do Django REST Framework.

    Métodos:
    - authenticate(request): Realiza a autenticação com base no token JWT presente no cabeçalho 'Authorization'
      da requisição.

    Exceções:
    - NotAuthenticated: Lançada se não houver token no cabeçalho da requisição.
    - PermissionDenied: Lançada se o token estiver expirado.
    - AuthenticationFailed: Lançada se ocorrerem problemas na decodificação do token.

    Atributos:
    - AUTHORIZATION: Nome da chave do cabeçalho utilizado para o token.
    """
    
    def authenticate(self, request) -> None:
    
        AUTHORIZATION = request.headers.get('Authorization')

        if not AUTHORIZATION:
            message = _('Sem Token - Bad Request')
            logger.error({'results': message})
            raise NotAuthenticated(message)

        try:
            jwt_token = AUTHORIZATION.split()
            jwt_token_decoded = decrypt_jwt_pass(jwt_token[1])
            request.jwt_token = jwt_token_decoded


        except jwt.ExpiredSignatureError as error:
            message = _('Token expirado!')
            logger.error({'results': message})
            logger.error(error)
            raise PermissionDenied(message)

        except jwt.InvalidSignatureError as error:
            message = _('Token invalido!')
            logger.error({'results': message})
            logger.error(error)
            raise AuthenticationFailed(message)

        except KeyError as error:
            message = _('Token invalido!')
            logger.error({'results': message})
            logger.error(error)
            raise AuthenticationFailed(message)

        except Exception as error:
            message = _('Token inesperado.')
            logger.error({'results': message})
            logger.error(error)
            raise AuthenticationFailed(message)




