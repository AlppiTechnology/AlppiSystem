#!/usr/bin/python
# -*- encoding: utf-8 -*-

import logging

logger = logging.getLogger('django')

def validate_cpf(cpf):

	# Verifica se o CPF possui 11 dígitos
	if len(cpf) != 11:
		logger.info('CPF não possui 11 dígitos')
		return False

	# Verifica se todos os dígitos são iguais
	if cpf == cpf[0] * 11:
		logger.info('CPF com dígitos iguais')
		return False

	# Validação do primeiro dígito verificador
	soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
	digito1 = (soma * 10) % 11 % 10
	if digito1 != int(cpf[9]):
		logger.info('Erro na validação do primeiro dígito verificador')
		return False

	# Validação do segundo dígito verificador
	soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
	digito2 = (soma * 10) % 11 % 10
	if digito2 != int(cpf[10]):
		logger.info('Erro na validação do segundo dígito verificador')
		return False

	return True


def validate_cnpj(cnpj):

	if len(cnpj) != 14 or cnpj == cnpj[0]*14:
		logger.info('CPF não possui 14 dígitos')
		return False
	
	# Verificação do primeiro dígito
	pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
	soma = sum(int(cnpj[i]) * pesos[i] for i in range(12))
	resto = soma % 11
	if resto < 2:
		if int(cnpj[12]) != 0:
			logger.info('Erro na validação do primeiro dígito verificador CNPJ 1')
			return False
	else:
		if int(cnpj[12]) != 11 - resto:
			logger.info('Erro na validação do primeiro dígito verificador CNPJ 2')
			return False
	
	# Verificação do segundo dígito
	pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
	soma = sum(int(cnpj[i]) * pesos[i] for i in range(13))
	resto = soma % 11
	if resto < 2:
		if int(cnpj[13]) != 0:
			logger.info('Erro na validação do segundo dígito verificador 1')
			return False
	else:
		if int(cnpj[13]) != 11 - resto:
			logger.info('Erro na validação do segundo dígito verificador 2')
			return False
	
	return True


def validate_cpf_cnpj(data):
	data = ''.join(filter(str.isdigit, data))
	logger.info(data)

	if len(data) == 11:
		return validate_cpf(data)
	elif len(data) == 14:
		print('aquiiii')
		print(data)
		return validate_cnpj(data)
	else:
		False