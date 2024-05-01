#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging
from django.db import connection

from alppi.jwt.jwt_encrypt import decrypt_jwt_modules

logger = logging.getLogger('django')

class SystemModules:

    def __init__(self) -> None:
        self.modules_jwt = None


    def get_modules(self) -> str:
        if os.path.exists('./alppi.key'):

            alppi_key: str = './alppi.key'
            with open(alppi_key, 'r') as arquivo:
                # Carregar o conteúdo do arquivo JSON
                self.modules_jwt = arquivo.read()

            return self.modules_jwt
        
        else:
            return None
        
    def set_modules(self, jwt_modules: str) -> str:
        try:
            if os.path.exists('./alppi.key'):

                alppi_key: str = './alppi.key'
                with open(alppi_key, 'w') as arquivo:
                    # Carregar o conteúdo do arquivo JSON
                    arquivo.write(jwt_modules)
                    return 'Modulos Atualizados com sucesso'

        except Exception as e:
            return f'Erro ao atualizar modulos: {e}'
        
    def update_system_modules(self) -> None:
        campus = self.get_campus_cnpj()

        if not campus:
            logger.error('Não foi encontrado nenhum campus para atualiza a Alppi.key.')

    def decoded_system_modules(self):
        modules = decrypt_jwt_modules(self.modules_jwt)
        return modules

    def get_campus_cnpj(self) -> dict:
        logger.info('Capturando CNPJ do campus.')
        query = 'SELECT cnpj FROM tb_campus'

        try:
            logger.info('Criando cursor no banco de dados')
            with connection.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()
                logger.info('Executando query get_campus_cnpj')

            return {'cnpj':row[0]}

        except Exception as error:
            message = 'Problemas do servidor ao atualizar acesso do usuario.'
            logger.info({'results': message})
            logger.error(error)
            return None


        finally:
            if cursor:
                cursor.close()
                logger.info('Cursor do banco fechado')

if __name__ == '__main__':
    SM = SystemModules()
    SM.update_system_modules()
