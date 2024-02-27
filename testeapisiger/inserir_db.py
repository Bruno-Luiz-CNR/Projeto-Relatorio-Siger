from conectarbanco import conexao_banco
import mysql.connector


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
            elif not resultado:
                # Se o resultado é None, faça uma inserção
                query = "INSERT INTO relpalacas.sigerrel (cliente, veiculos) VALUES (%s, %s)"
                dados = (cliente_str, placa_str)
            else:
                # Não faça nada se o resultado for igual a cliente_str
                print("Nada foi incluído")

            if query and dados:
                cursor.execute(query, dados)
                conexao.commit()

        except mysql.connector.Error as err:
            print(f'Erro durante a inserção/atualização do cliente: {err}')

        finally:
            # Certifique-se de fechar a conexão e o cursor ao finalizar
            if conexao.is_connected():
                cursor.close()
                conexao.close()


# O restante do seu código permanece inalterado
