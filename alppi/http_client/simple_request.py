#!/usr/bin/python
# -*- encoding: utf-8 -*-
import requests, logging, json

logger = logging.getLogger('django')


class HttpClient:
    """
    Cliente HTTP para realizar requisições a uma API.

    Esta classe oferece métodos simples para realizar requisições HTTP (GET, POST, PUT, DELETE)
    para um endpoint específico em uma API. Ela utiliza a biblioteca `requests` para lidar com as requisições.

    Métodos Públicos:
    - get(endpoint, params=None, headers=None, cookies=None, auth=None): Realiza uma requisição GET.
    - post(endpoint, data=None, headers=None, cookies=None, auth=None): Realiza uma requisição POST.
    - put(endpoint, data=None, headers=None, cookies=None, auth=None): Realiza uma requisição PUT.
    - delete(endpoint, headers=None, cookies=None, auth=None): Realiza uma requisição DELETE.

    Parâmetros:
    - base_url (str): A URL base da API.
    - default_headers (dict): Cabeçalhos padrão a serem incluídos em todas as requisições.

    Exceções:
    - HttpException: Lançada em caso de erro durante a requisição HTTP.
    """
    def __init__(self, base_url, default_headers=None):
        self.base_url = base_url
        self.default_headers = default_headers or {}
        self.response = None

    def _make_request(self, method, endpoint, params=None, json=None, data=None, headers=None, cookies=None, auth=None) -> str | dict:
        """
        Realiza uma requisição HTTP.

        Parâmetros:
        - method (str): O método HTTP da requisição (GET, POST, PUT, DELETE).
        - endpoint (str): O endpoint específico da API.
        - params (dict): Parâmetros da requisição (para GET).
        - data (dict): Dados da requisição (para POST e PUT).
        - headers (dict): Cabeçalhos específicos da requisição.
        - cookies (dict): Cookies da requisição.
        - auth (tuple): Tupla de autenticação (usuário, senha).

        Retorna:
        str or dict: A resposta da requisição em formato de texto ou JSON.

        Exceções:
        - HttpException: Lançada em caso de erro durante a requisição HTTP.
        """
        url = f"{self.base_url}/{endpoint}"
        final_headers = {**self.default_headers, **(headers or {})}
        
        try:
            self.response = requests.request(
                method,
                url,
                json=json,
                params=params,
                data=data,
                headers=final_headers,
                cookies=cookies,
                auth=auth
            )
            
            self.response.raise_for_status()  # Lança exceção se a resposta indicar um erro HTTP

            return self.response.json() if self.response.headers.get('content-type') == 'application/json' else self.response.text
        except requests.exceptions.RequestException as e:
            # Trata exceções relacionadas a problemas de rede ou respostas HTTP de erro
            if self.response == None:
                response = {}
                response['results'] = 'Microsservice não responde...'
            else:
                response = self.response.json()

            raise HttpException(f"Erro na requisição HTTP: {str(e)}. {response.get('results')}")

    def get(self, endpoint, params=None, headers=None, cookies=None, auth=None) -> str | dict:
        """
        Realiza uma requisição GET.

        Parâmetros:
        - endpoint (str): O endpoint específico da API.
        - params (dict): Parâmetros da requisição.

        Retorna:
        str or dict: A resposta da requisição em formato de texto ou JSON.
        """
        return self._make_request("GET", endpoint, params=params, headers=headers, cookies=cookies, auth=auth)

    def post(self, endpoint, json=None, data=None, headers=None, cookies=None, auth=None) -> str | dict:
        """
        Realiza uma requisição POST.

        Parâmetros:
        - endpoint (str): O endpoint específico da API.
        - data (dict): Dados da requisição.

        Retorna:
        str or dict: A resposta da requisição em formato de texto ou JSON.
        """
        return self._make_request("POST", endpoint, json=json, data=data, headers=headers, cookies=cookies, auth=auth)

    def put(self, endpoint, json=None, data=None, headers=None, cookies=None, auth=None) -> str | dict:
        """
        Realiza uma requisição PUT.

        Parâmetros:
        - endpoint (str): O endpoint específico da API.
        - data (dict): Dados da requisição.

        Retorna:
        str or dict: A resposta da requisição em formato de texto ou JSON.
        """
        return self._make_request("PUT", endpoint, json=json, data=data, headers=headers, cookies=cookies, auth=auth)

    def delete(self, endpoint, headers=None, cookies=None, auth=None) -> str | dict:
        """
        Realiza uma requisição DELETE.

        Parâmetros:
        - endpoint (str): O endpoint específico da API.

        Retorna:
        str or dict: A resposta da requisição em formato de texto ou JSON.
        """
        return self._make_request("DELETE", endpoint, headers=headers, cookies=cookies, auth=auth)

class HttpException(Exception):
    pass
