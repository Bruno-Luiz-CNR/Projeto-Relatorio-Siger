import mysql.connector


def conexao_banco():
    config = {
        'user': 'root',
        'password': 'bruno1991@',
        'host': 'localhost',
        'database': 'dbdados_siger',
        'raise_on_warnings': True,
    }

    try:
        conexao = mysql.connector.connect(**config)
        if conexao.is_connected():
            cursor = conexao.cursor()
            print('Conexão bem-sucedida!')
            return cursor

    except mysql.connector.Error as err:
        print(f'Erro: {err}')

    finally:
        # Certifique-se de fechar a conexão ao finalizar
        if 'connection' in locals() and conexao.is_connected():
            conexao.close()
            print('Conexão encerrada.')