import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import datetime


def verifica_conexao():
    try:
        # Configurar o Chrome em modo headless
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)

        # Tente abrir um site que geralmente está acessível
        driver.get("http://www.google.com")

        data_hora_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logging.basicConfig(filename='log_file.log', level=logging.INFO)
        logging.info(f'{data_hora_atual} CONEXÃO REALIZADA COM SUCESSO, PROCESSANDO INSERÇÕES E ALTERAÇÕES!')

        driver.quit()
        return True
    except WebDriverException as e:
        logging.error(f'Erro ao verificar conexão: {str(e)}')
        return False
