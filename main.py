import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from typing import List


def main():
    # Use o ChromeDriverManager para baixar automaticamente o ChromeDriver
    url_rotas = "https://siger.winksys.com.br:8443/#consultaequipamento"

    chrome_options = webdriver.ChromeOptions()
    # Não adiciona a opção "--headless" para desativar o modo headless
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    # Chame o ChromeDriverManager sem usar o método install()

    driver.maximize_window()
    driver.get(url_rotas)
    wait = WebDriverWait(driver, 30)

    inputlogin = wait.until(ec.visibility_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div/div/div[4]'
                                                                       '/form/div/div[1]/input')))
    inputlogin.send_keys("seuusuario")
    inputsenha = wait.until(ec.visibility_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div/div'
                                                                       '/div[4]/form/div/div[2]/input')))
    inputsenha.send_keys("suasenha")
    driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div/div[4]/form/div/div[3]/button').click()
    abrircadastro = wait.until(ec.visibility_of_element_located(
        (By.XPATH,'/html/body/div[3]/div[1]/div[5]/div[1]/div[1]/div[1]')))
    abrircadastro.click()
    abrirequipamento = wait.until(ec.visibility_of_element_located(
        (By.XPATH,'/html/body/div[3]/div[1]/div[5]/div[1]/div[2]/a[6]')))
    abrirequipamento.click()
    # desabilitar checkbox
    cbdefeito = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="gwt-uid-81"]')))
    cbdefeito.click()
    cbbaixado = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="gwt-uid-80"]')))
    cbbaixado.click()
    cbvinculado = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="gwt-uid-78"]')))
    cbvinculado.click()
    btndisponivel = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="gwt-uid-77"]')))
    btndisponivel.click()
    btnpesquisar = wait.until(ec.visibility_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/button')))
    btnpesquisar.click()
    # paginação
    elementos_paginacao = driver.find_elements(By.CLASS_NAME, "gwt-Label.dib.link.pad5")
    time.sleep(2)
    for elemento in elementos_paginacao:
        # Construa o seletor XPath para a página específica
        xpath_pagina = f'/html/body/div[3]/div[2]/div/div[4]/div[{elemento.text}]'
        clicarpagina = wait.until(ec.visibility_of_element_located((By.XPATH, xpath_pagina)))
        clicarpagina.click()
        time.sleep(5)

        # Aguarde até que a tabela esteja presente na página atual
        classe_da_tabela = "mt5.grid"  # Remova o espaço entre as classes
        tabela_presente: WebElement = WebDriverWait(driver, 30).until(
            ec.presence_of_element_located((By.CLASS_NAME, classe_da_tabela))
        )

        # Localizar todas as linhas da tabela, excluindo a primeira (cabeçalho)
        linhas: List[WebElement] = tabela_presente.find_elements(By.TAG_NAME, "tr")[1:]
        time.sleep(1)
        # Iterar sobre as linhas e fazer o que for necessário com cada uma
        for linha in linhas:
            try:
                # Tente localizar novamente as células na linha para evitar o erro StaleElementReferenceException
                celulas: List[WebElement] = linha.find_elements(By.TAG_NAME, "td")[1:]

                # Verifique se há células suficientes antes de acessar os índices
                if len(celulas) >= 1:  # Verifique se há pelo menos 13 células na linha
                    fabricante = celulas[2].text
                    fornecedor = celulas[3].text
                    numero = celulas[4].text
                    operadora = celulas[6].text
                    linha = celulas[7].text
                    veiculo = celulas[11].text
                    modelo = celulas[12].text

                    print(
                        f"Fabricante: {fabricante}, Fornecedor: {fornecedor}, Número: {numero}, Operadora: "
                        f"{operadora}, Linha: {linha}, Veículo: {veiculo}, Modelo: {modelo}")

                else:
                    print("Número insuficiente de células na linha")

            except Exception as e:
                print(f"Erro ao processar uma linha: {e}")

            # Aguarde um curto período de tempo para permitir que a página role completamente


if __name__ == "__main__":
    main()
    
