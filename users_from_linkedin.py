# Importar os módulos necessários 
import csv 
import time 
import json
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys

# Importar as credenciais do usuários de um arquivo de configuração
with open('config.json', 'r') as f:
    credentials  = json.load(f)

 
# Configurar o driver do Selenium (neste caso, para o navegador Chrome) 
driver = webdriver.Chrome() 
 
# Fazer login no LinkedIn 
driver.get("https://www.linkedin.com/login") 
username_input = driver.find_element(By.ID, "username") 
password_input = driver.find_element(By.ID, "password") 
username_input.send_keys(credentials['email']) # Substituir pelo seu email 
password_input.send_keys(credentials['password']) # Substituir pela sua senha  
password_input.send_keys(Keys.RETURN) 
time.sleep(3) 
 
# Acessar a página de pesquisa de pessoas do LinkedIn 
driver.get("https://www.linkedin.com/search/results/people/?keywords=&origin=FACETED_SEARCH")
time.sleep(3) 

# Preencher o campo de busca com a cidade de João Pessoa 
location = driver.find_element(By.XPATH, "//button[@aria-label='Filtro Localidades. Clicar neste botão exibe todas as opções de filtro de Localidades.']") 
location.click() 
location_input = driver.find_element(By.XPATH, "//input[@aria-label='Adicionar localidade']") 
location_input.send_keys("João Pessoa")
time.sleep(3) 
location_input.send_keys(Keys.ARROW_DOWN)
location_input.send_keys(Keys.RETURN)
location_input.send_keys(Keys.ESCAPE)
time.sleep(3)
show_results_button = driver.find_element(By.XPATH, "//body/div[5]/div[3]/div[2]/section[1]/div[1]/nav[1]/div[1]/ul[1]/li[4]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/fieldset[1]/div[2]/button[2]/span[1]") 
show_results_button.click()
time.sleep(3) 
 
# Capturar as informações das pessoas encontradas 
people = driver.find_elements(By.CSS_SELECTOR, "ul[class='reusable-search__entity-result-list list-style-none'] > li")
print(people)  
 
# Exportar as informações para um arquivo CSV 
with open('people_joao_pessoa_linkedin.csv', 'w', encoding="utf-8", newline='') as file: 
    writer = csv.writer(file) 
    writer.writerow(["Nome", "Cargo", "Localização"]) 
 
    for person in people: 
        name = person.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text
        print(name)
        
        try: 
            title = person.find_element(By.CSS_SELECTOR, "div[class='entity-result__primary-subtitle t-14 t-black t-normal']").text 
        except: 
            title = "" 
        try: 
            location = person.find_element(By.CSS_SELECTOR, "div[class='entity-result__secondary-subtitle t-14 t-normal']").text 
        except: 
            location = "" 
 
        writer.writerow([name, title, location]) 
 
# Fechar o driver do Selenium 
driver.quit()