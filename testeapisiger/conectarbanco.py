import mysql.connector
import logging


def conexao_banco():
    config = {
        'user': 'root',
        'password': 'Bcllick2024@',
        'host': 'localhost',
        'database': 'api_siger',
        'raise_on_warnings': True,
    }

    try:
        conexao = mysql.connector.connect(**config, autocommit=True)
        if conexao.is_connected():
            cursor = conexao.cursor()
            return conexao, cursor

    except mysql.connector.Error as err:
        logging.error(f'Erro durante a conexão com o banco de dados: {err}')

    return None, None

