from conectarbanco import conexao_banco
import mysql.connector
import logging

logging.basicConfig(filename='log_insercao.log', level=logging.INFO)


def converter_para_string(valor):
    if isinstance(valor, list):
        # Se for uma lista, retorne a primeira entrada
        return str(valor[0]) if valor else "VALOR NAO CADASTRADO"
    else:
        # Se não for uma lista, apenas retorne o valor como string
        return str(valor) if valor else "VALOR NAO CADASTRADO"


def incluclie(placa, cliente):
    cliente_str = converter_para_string(cliente)
    placa_str = converter_para_string(placa).replace(" ", "")

    conexao, cursor = conexao_banco()

    if conexao and cursor:
        query = None
        dados = None

        try:
            query_verificar = "SELECT cliente FROM relpalacas.sigerrel WHERE veiculos = %s"
            cursor.execute(query_verificar, (placa_str,))
            resultado = cursor.fetchone()

            if resultado and resultado[0] != cliente:
                # Se a placa já existe e o cliente é diferente, faça um UPDATE
                query = "UPDATE relpalacas.sigerrel SET cliente = %s WHERE veiculos = %s"
                dados = (cliente_str, placa_str)
                logging.info(f'Cliente atualizado: {cliente_str}, {placa_str}')
                print("Dados Atualizados: ", cliente_str, placa_str)
            elif not resultado:
                # Se o resultado é None, faça uma inserção
                query = "INSERT INTO relpalacas.sigerrel (cliente, veiculos) VALUES (%s, %s)"
                dados = (cliente_str, placa_str)
                logging.info(f'Novo cliente inserido: {cliente_str}, {placa_str}')
                print("Dados Incluidos: ", cliente_str, placa_str)
            else:
                # Não faça nada se o resultado for igual a cliente_str
                logging.info(f'Nenhuma ação necessária: {cliente_str}, {placa_str}')
                print("Nenhuma ação necessária")

            if query and dados:
                cursor.execute(query, dados)
                conexao.commit()

        except mysql.connector.Error as err:
            logging.error(f'Erro durante a inserção/atualização cliente: {err}')

        finally:
            # Certifique-se de fechar a conexão e o cursor ao finalizar
            if conexao.is_connected():
                cursor.close()
                conexao.close()


