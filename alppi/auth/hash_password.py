#!/usr/bin/python
# -*- encoding: utf-8 -*-

# ╔══╗╔══╗─╔══╗╔══╗╔╗──╔═══╗╔════╗╔══╗
# ║╔╗║║╔╗║─║╔═╝║╔╗║║║──║╔══╝╚═╗╔═╝║╔╗║
# ║║║║║╚╝╚╗║╚═╗║║║║║║──║╚══╗──║║──║║║║
# ║║║║║╔═╗║╚═╗║║║║║║║──║╔══╝──║║──║║║║
# ║╚╝║║╚═╝║╔═╝║║╚╝║║╚═╗║╚══╗──║║──║╚╝║
# ╚══╝╚═══╝╚══╝╚══╝╚══╝╚═══╝──╚╝──╚══╝


import bcrypt, logging

logger = logging.getLogger('django')

def encrypt_data(passwd) -> str:
    """
    Criptografa a senha de entrada usando bcrypt.

    Esta função utiliza o algoritmo bcrypt para criptografar a senha de entrada.
    O processo inclui a geração de um salt aleatório, que é então utilizado na
    criação do hash da senha.

    Parâmetros:
    - passwd (str): A senha a ser criptografada.

    Retorna:
    str: A senha criptografada.

    Exceções:
    - Exception: Lançada em caso de erro durante o processo de criptografia.

    Notas:
    - O salt é gerado automaticamente pelo bcrypt.
    """
    try:
        logger.debug('Criptografando senha')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwd.encode('utf-8'), salt)
        
        return hashed.decode('utf-8')
    except:
        logger.error('Erro ao criptografar senha')
        raise Exception('Erro ao criptografar senha')



def veryfy_pass(password, password_db) -> bool:
    """
    Verifica se as senhas são iguais após a criptografia.

    Esta função compara a senha fornecida com a senha armazenada no banco de dados,
    ambas criptografadas usando o algoritmo bcrypt.

    Parâmetros:
    - password (str): A senha a ser verificada.
    - password_db (str): A senha armazenada no banco de dados.

    Retorna:
    bool: True se as senhas são iguais, False caso contrário.
    """
    is_equal = bcrypt.hashpw(password.encode('utf-8'), password_db.encode('utf-8')) == password_db.encode('utf-8')

    return is_equal
