from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def extrair_informacoes_linha(linha):
    try:
        veiculo = linha.find_element(By.XPATH, './/td[contains(@class, "veiculo")]').text
    except NoSuchElementException:
        veiculo = None

    try:
        fabricante = linha.find_element(By.XPATH, './/td[contains(@class, "fabricante")]').text
    except NoSuchElementException:
        fabricante = None

    try:
        numero = linha.find_element(By.XPATH, './/td[contains(@class, "numero")]').text
    except NoSuchElementException:
        numero = None

    try:
        linha_info = linha.find_element(By.XPATH, './/td[contains(@class, "linha")]').text
    except NoSuchElementException:
        linha_info = None

    try:
        operadora = linha.find_element(By.XPATH, './/td[contains(@class, "operadora")]').text
    except NoSuchElementException:
        operadora = None

    return veiculo, fabricante, numero, linha_info, operadora
