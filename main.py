import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import sys
from inserirdados import inserir_dados
from verificonexao import verifica_conexao
from main2 import iniciarmain2
import logging
import datetime


def apaga_log_anterior():
    log_file = 'log_insercao.log'

    # Abre o arquivo de log em modo de escrita ('w') para limpar o conteúdo
    with open(log_file, 'w'):
        pass

    # Configuração do logging
    logging.basicConfig(filename=log_file, level=logging.INFO)


def main():

    while not verifica_conexao():
        data_hora_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.basicConfig(filename='log_file.log', level=logging.INFO)
        logging.error(f'{data_hora_atual} Sem conexão com a internet. Tentando reconectar em 10 segundos...')
        time.sleep(30)

    # Use o ChromeDriverManager para baixar automaticamente o ChromeDriver
    #url_rotas = "https://siger.winksys.com.br:8443/#consultaequipamento"
    #chrome_options = webdriver.ChromeOptions()
    #driver = webdriver.Chrome(options=chrome_options)
    #driver.maximize_window()
    #driver.get(url_rotas)
    #wait = WebDriverWait(driver, 120)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')  # Ajuste o tamanho da janela conforme necessário
    chrome_options.add_argument('--start-maximized')

    # Use o ChromeDriverManager para baixar automaticamente o ChromeDriver
    url_rotas = "https://siger.winksys.com.br:8443/#consultaequipamento"
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_rotas)
    wait = WebDriverWait(driver, 120)

    inputlogin = wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/div/div[4]'
                                                                        '/form/div/div[1]/input')))
    inputlogin.send_keys("Seu login")
    inputsenha = wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/div'
                                                                        '/div[4]/form/div/div[2]/input')))
    inputsenha.send_keys("Sua senha")
    driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div[4]/form/div/div[3]/button').click()
    time.sleep(1)
    abrircadastro = wait.until(ec.visibility_of_element_located(
        (By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[1]/div[1]/div[1]')))
    abrircadastro.click()
    abrirequipamento = wait.until(ec.visibility_of_element_located(
        (By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[1]/div[2]/a[6]')))
    abrirequipamento.click()
    # desabilitar checkbox
    cbdefeito = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="gwt-uid-83"]')))
    cbdefeito.click()
    cbbaixado = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="gwt-uid-82"]')))
    cbbaixado.click()
    cbvinculado = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="gwt-uid-80"]')))
    cbvinculado.click()
    btndisponivel = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="gwt-uid-79"]')))
    btndisponivel.click()

    btnpesquisar = wait.until(
        ec.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/button')))
    btnpesquisar.click()
    # paginação

    elementos_numeros = WebDriverWait(driver, 18).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.paginador div.gwt-Label'))
    )

    # Converta os elementos para números antes do loop
    numeros = [int(elemento.text.strip()) for elemento in elementos_numeros]

    # Iterar sobre os números e capturar um por vez
    for numero in numeros:

        try:

            mudarpagina = wait.until(
                ec.element_to_be_clickable((By.XPATH, f'/html/body/div[3]/div[2]/div/div[4]/div[{numero}]')))
            mudarpagina.click()
            time.sleep(18)

            classe_da_tabela = "mt5.grid"
            tabela_presente = WebDriverWait(driver, 30).until(
                ec.presence_of_element_located((By.CLASS_NAME, classe_da_tabela))
            )

            # Localizar todas as linhas da tabela, excluindo a primeira (cabeçalho)
            linhas: List[WebElement] = tabela_presente.find_elements(By.TAG_NAME, "tr")[1:]
            if not linhas:
                break
            # Iterar sobre as linhas e fazer o que for necessário com cada uma
            for linha in linhas:
                driver.execute_script("arguments[0].scrollIntoView();", linha)
                try:
                    # Tente localizar novamente as células na linha para evitar o erro
                    # StaleElementReferenceException
                    celulas: List[WebElement] = linha.find_elements(By.TAG_NAME, "td")

                    # Verifique se há células suficientes antes de acessar os índices
                    if len(celulas) > 15:
                        fabricante = celulas[3].text
                        if not fabricante:
                            fabricante = "FABRICANTE NAO CADASTRADO"

                        fornecedor = celulas[4].text
                        if not fornecedor:
                            fornecedor = "FORNECEDOR NAO CADASTRADO"

                        numero = celulas[5].text.split()
                        if not numero:
                            numero = "NUMERO NAO CADASTRADO"

                        operadora = celulas[7].text.split()
                        if not operadora:
                            operadora = "OPERADORA NAO CADASTRADA"

                        linha = ''.join(filter(str.isdigit, celulas[8].text))
                        if not linha:
                            linha = "LINHA NAO CADASTRADA"

                        placa = celulas[12].text
                        if not placa:
                            placa = "PLACA NAO CADASTRADA"

                        modelo = celulas[13].text.split()
                        if not modelo:
                            modelo = "MODELO NAO CADASTRADO"

                        inserir_dados(fabricante, fornecedor, numero, operadora, linha, placa, modelo)
                    else:
                        fabricante = celulas[2].text
                        if not fabricante:
                            fabricante = "FABRICANTE NAO CADASTRADO"

                        fornecedor = celulas[3].text
                        if not fornecedor:
                            fornecedor = "FORNECEDOR NAO CADASTRADO"

                        numero = celulas[4].text.split()
                        if not numero:
                            numero = "NUMERO NAO CADASTRADO"

                        operadora = celulas[6].text.split()
                        if not operadora:
                            operadora = "OPERADORA NAO CADASTRADA"

                        linha = ''.join(filter(str.isdigit, celulas[7].text))
                        if not linha:
                            linha = "LINHA NAO CADASTRADA"

                        placa = celulas[11].text
                        if not placa:
                            placa = "PLACA NAO CADASTRADA"

                        modelo = celulas[12].text.split()
                        if not modelo:
                            modelo = "MODELO NAO CADASTRADO"

                        inserir_dados(fabricante, fornecedor, numero, operadora, linha, placa, modelo)

                except Exception:
                    pass

        except Exception:
            pass
    print("Não há mais elementos para iterar. Chamar 'CADASTRO DE CLIENTE' e sair.")
    logging.info('Não há mais elementos para iterar. Chamar CADASTRO DE CLIENTE e sair.')
    driver.quit()
    iniciarmain2()


if __name__ == "__main__":
    apaga_log_anterior()
    main()
    logging.shutdown()
    sys.exit()
