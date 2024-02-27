import mysql.connector
import logging

logging.basicConfig(filename='log_insercao.log', level=logging.INFO)


def conexao_banco():
    config = {
        'user': 'root',
        'password': 'login',
        'host': 'localhost',
        'database': 'db',
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
