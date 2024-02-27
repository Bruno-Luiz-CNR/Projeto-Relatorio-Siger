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


def inserir_dados(fabricante, fornecedor, numero, operadora, linha, placa, modelo):
    fabricante_str = converter_para_string(fabricante)
    fornecedor_str = converter_para_string(fornecedor)
    numero_str = converter_para_string(numero)
    operadora_str = converter_para_string(operadora)
    linha_str = converter_para_string(linha)
    placa_str = converter_para_string(placa)
    modelo_str = converter_para_string(modelo)
    conexao, cursor = conexao_banco()

    if conexao and cursor:
        try:
            # Verifica se a placa já existe no banco de dados
            query_verificar = "SELECT veiculos FROM sigerrel WHERE veiculos = %s"
            cursor.execute(query_verificar, (placa_str,))
            resultado = cursor.fetchone()

            if resultado:
                # Se a placa já existe, faça um UPDATE
                query = ("UPDATE sigerrel SET fabricante = %s, fornecedor = %s, numero = %s, "
                         "operadora = %s, linha = %s, modelo = %s "
                         "WHERE veiculos = %s")
                dados = (fabricante_str, fornecedor_str, numero_str, operadora_str, linha_str, modelo_str, placa_str)
                logging.info(f'Dados atualizados: {fabricante_str}, {fornecedor_str}, {numero_str}, {operadora_str}, '
                             f'{linha_str}, {placa_str}, {modelo_str}')
            else:
                # Se a placa não existe, faça um INSERT
                query = ("INSERT INTO sigerrel "
                         "(fabricante, fornecedor, numero, operadora, linha, veiculos, modelo) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s)")
                dados = (fabricante_str, fornecedor_str, numero_str, operadora_str, linha_str, placa_str, modelo_str)
                logging.info(f'Dados Inseridos: {fabricante_str}, {fornecedor_str}, {numero_str}, {operadora}, '
                             f'{linha_str}, {placa_str}, {modelo_str}')

            # Execute o comando de INSERT ou UPDATE
            query_str = query % tuple(dados)
            print("Query:", query_str)
            cursor.execute(query, dados)

        except mysql.connector.Error as err:
            logging.error(f'Erro durante a inserção/atualização: {err}')

        finally:
            # Certifique-se de fechar a conexão e o cursor ao finalizar
            if conexao.is_connected():
                cursor.close()
                conexao.close()



