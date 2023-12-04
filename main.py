from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.chrome.options import Options

import time



link = "https://www.google.com/maps/search/restaurante+sao+jose+dos+campos/@-23.1798115,-45.8838093,13z/data=!4m2!2m1!6e5?entry=ttu"

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
browser = webdriver.Chrome(options=chrome_options)


record = []
e = []



def extrair_informacoes(html_lista):
    endereco = None
    telefone = None
    site = None
    items = []
    for item in html_lista:
        items.append(item.text)
    for item in items:
        if '122' in item:
            endereco = item
        if '(12)' in item:
            telefone = item
        if '.com' in item:
            site = item

    return endereco, telefone, site

def extrair_avalicacoes(html_lista):
    estrelas = None
    avaliacoes = None

    for item in html_lista:
        estrelas = item.text[0:3]
        avaliacoes = item.text.split('(', 1)[-1].split(')', 1)[0]

    return estrelas, avaliacoes

def Selenium_extractor():
    global le
    time.sleep(5)
    action = ActionChains(browser)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")
    while len(a) < 7:
        print(len(a))
        var = len(a)
        scroll_origin = ScrollOrigin.from_element(a[len(a)-1])
        action.scroll_from_origin(scroll_origin, 0, 1000).perform()

        a = browser.find_elements(By.CLASS_NAME, "hfpxzc")
        if len(a) == var:
            le+=1
            if le > 20:
                break
        else:
            le = 0

    for i in range(len(a)):

        scroll_origin = ScrollOrigin.from_element(a[i])
        action.scroll_from_origin(scroll_origin, 0, 100).perform()
        action.move_to_element(a[i]).perform()
        a[i].click()
        time.sleep(2)
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')
        try:
            Name_Html = soup.findAll('h1', {"class": "DUwDvf lfPIob"})
            Endereco_Html = soup.findAll('div', {"class": "Io6YTe fontBodyMedium kR99db"})
            Avaliacao_Html = soup.findAll('div', {'class': 'LBgpqf'})

            name = Name_Html[0].text



            """print(endereco)
            print(site)
            print(telefone)
            print(Endereco_Html)"""
            endereco, telefone, site = extrair_informacoes(Endereco_Html)
            estrelas, avaliacoes = extrair_avalicacoes(Avaliacao_Html)
            print(f"Restaurante: {name}\nEndereço: {endereco}\nSite: {site}\nTelefone: {telefone}"
                  f"\nEstrelas: {estrelas}\nAvaliações: {avaliacoes}")

            print("\n")
        except:
            print("\n")
            continue


le = 0
browser.get(str(link))
time.sleep(10)
Selenium_extractor()
