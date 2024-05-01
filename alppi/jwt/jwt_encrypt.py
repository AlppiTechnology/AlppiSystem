#!/usr/bin/python
# -*- encoding: utf-8 -*-
import jwt, logging
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger('django')
RS256 = 'RS256'

# -------------- PASSWORD ------------------

def create_jwt_pass(data) -> str:
    """
    Cria um token JWT com os dados fornecidos.

    Esta função cria um token JWT utilizando uma chave privada RSA. Os dados fornecidos são utilizados como payload.

    Parâmetros:
    - data (dict): Os dados a serem incluídos no payload do token.

    Retorna:
    str: O token JWT criado.

    Exceções:
    - FileNotFoundError: Se o arquivo contendo a chave privada não for encontrado.
    """
    logger.debug('Criando Token JWT')
    private_rsa = read_rsa_pass()

    private_key = serialization.load_ssh_private_key(
    private_rsa, password=b''
    )
    
    encoded = jwt.encode(payload=data, key=private_key, algorithm=RS256)
    return encoded
    # return encoded.decode('utf-8') antiga lib precisava decodar


def decrypt_jwt_pass(jwt_encoded) -> dict:
    """
    Decodifica um token JWT e retorna o payload como um dicionário.

    Esta função decodifica um token JWT utilizando uma chave pública RSA.

    Parâmetros:
    - jwt_encoded (str): O token JWT a ser decodificado.

    Retorna:
    dict: O payload decodificado do token JWT.
    
    Exceções:
    - jwt.DecodeError: Se o token JWT não puder ser decodificado.
    - FileNotFoundError: Se o arquivo contendo a chave pública não for encontrado.
    """
    pulic_rsa = read_pulic_pass()
    decoded = jwt.decode(jwt_encoded, pulic_rsa, algorithms=[RS256] )
    return decoded


def read_rsa_pass() -> bytes:
    """
    Lê e retorna o conteúdo do arquivo contendo a chave privada RSA.

    Retorna:
    bytes: O conteúdo do arquivo da chave privada RSA.

    Exceções:
    - FileNotFoundError: Se o arquivo contendo a chave privada não for encontrado.
    """
    private_key = open('./id_rsa_pass', 'rb').read()
    return private_key


def read_pulic_pass() -> bytes:
    """
    Lê e retorna o conteúdo do arquivo contendo a chave pública RSA.

    Retorna:
    bytes: O conteúdo do arquivo da chave pública RSA.

    Exceções:
    - FileNotFoundError: Se o arquivo contendo a chave privada não for encontrado.
    """
    public_key = open('./id_rsa_pass.pub', 'rb').read()
    return public_key

# -------------- MODULES ------------------

def encrypt_jwt_modules(data) -> str:
    """
    Cria um token JWT com os dados fornecidos.

    Esta função cria um token JWT utilizando uma chave privada RSA. Os dados fornecidos são utilizados como payload.

    Parâmetros:
    - data (dict): Os dados a serem incluídos no payload do token.

    Retorna:
    str: O token JWT criado.

    Exceções:
    - FileNotFoundError: Se o arquivo contendo a chave privada não for encontrado.
    """
    logger.debug('Criando Token JWT')
    private_rsa = read_rsa_modules()

    private_key = serialization.load_ssh_private_key(
    private_rsa, password=b''
    )
    
    encoded = jwt.encode(payload=data, key=private_key, algorithm=RS256)
    return encoded


def decrypt_jwt_modules(jwt_encoded) -> dict:
    """
    Decodifica um token JWT e retorna o payload como um dicionário.

    Esta função decodifica um token JWT utilizando uma chave pública RSA.

    Parâmetros:
    - jwt_encoded (str): O token JWT a ser decodificado.

    Retorna:
    dict: O payload decodificado do token JWT.
    
    Exceções:
    - jwt.DecodeError: Se o token JWT não puder ser decodificado.
    - FileNotFoundError: Se o arquivo contendo a chave pública não for encontrado.
    """
    pulic_rsa = read_pulic_modules()
    decoded = jwt.decode(jwt_encoded, pulic_rsa, algorithms=[RS256] )
    return decoded


def read_rsa_modules() -> bytes:
    """
    Lê e retorna o conteúdo do arquivo contendo a chave privada RSA.

    Retorna:
    bytes: O conteúdo do arquivo da chave privada RSA.

    Exceções:
    - FileNotFoundError: Se o arquivo contendo a chave privada não for encontrado.
    """
    private_key = open('./id_rsa_modules', 'rb').read()
    return private_key


def read_pulic_modules() -> bytes:
    """
    Lê e retorna o conteúdo do arquivo contendo a chave pública RSA.

    Retorna:
    bytes: O conteúdo do arquivo da chave pública RSA.

    Exceções:
    - FileNotFoundError: Se o arquivo contendo a chave privada não for encontrado.
    """
    public_key = open('./id_rsa_modules.pub', 'rb').read()
    return public_key
