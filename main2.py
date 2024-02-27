import requests
import json
from inserir_db import incluclie
from datetime import datetime


# Função para obter o token de autenticação
def obter_token():
    url = "http://siger.winksys.com.br:8000/gateway/api/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "token": "seu token"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception(f"Falha ao obter token. Código de resposta: {response.status_code}")


# Função para consultar veículos de todos os clientes usando o token
def consultar_veiculos(token):
    url = "http://siger.winksys.com.br:8000/gateway/api/cadastros/consulta/veiculos"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    pagina = 0
    cobranca_ativa = True
    rastreado = True

    while True:
        data = {
            "pagina": pagina,
            "cobrancaAtiva": cobranca_ativa,
            "rastreado": rastreado
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            resultado = response.json()

            # Processar os resultados da página atual
            processar_resultado_consulta(resultado)

            # Verificar se há mais páginas
            pagina += 1
            if pagina >= resultado["qtdPaginas"]:
                break
        else:
            raise Exception(f"Falha ao consultar veículos. Código de resposta: {response.status_code}")


# Função para processar o resultado da consulta
def processar_resultado_consulta(resultado):
    veiculos = resultado.get('veiculos', [])
    for veiculo in veiculos:
        placa = veiculo.get('placa', 'N/A')
        cliente = veiculo.get('cliente', {}).get('nome', 'N/A')

        incluclie(placa, cliente)


def iniciarmain2():
    # Obter token
    token = obter_token()

    # Consultar veículos usando o token
    consultar_veiculos(token)
