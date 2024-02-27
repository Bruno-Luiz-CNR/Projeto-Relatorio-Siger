import requests
import json
from inserir_db import incluclie
from datetime import datetime


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


def consultar_equipamentos(token):
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
            processar_resultado_consulta(resultado)
            pagina += 1
            if pagina >= resultado["qtdPaginas"]:
                break
        else:
            raise Exception(f"Falha ao consultar equipamentos. Código de resposta: {response.status_code}")


def processar_resultado_consulta(resultado):
    equipamentos = resultado.get('equipamentos', [])
    print(equipamentos)
    for equipamento in equipamentos:
        numero = equipamento.get('numero', 'N/A')
        descricao = equipamento.get('descricao', 'N/A')

        # Faça o que precisar com as informações do equipamento
        print(f'Número: {numero}, Descrição: {descricao}')


# Obter token
token = obter_token()

# Consultar equipamentos usando o token
consultar_equipamentos(token)
