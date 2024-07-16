from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = webdriver.Edge()

driver.get("https://www.mercadolibre.com.mx/")
time.sleep(5)

input1 = driver.find_element(By.ID, "cb1-edit")
input1.send_keys("Computadora")
time.sleep(5)

submit_button = driver.find_element(By.CLASS_NAME, "nav-icon-search")
submit_button.click()
time.sleep(5)

all_data = []

search_results = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ui-search-results"))
)

product_cards = driver.find_elements(By.CLASS_NAME, "andes-card")

for card in product_cards:
    try:
        title = card.find_element(By.CLASS_NAME, "ui-search-item__title").text
    except:
        title = "No disponible"
    
    try:
        price = card.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
    except:
        price = "No disponible"
    
    if title != "No disponible" and price != "No disponible":
        all_data.append([title, price])

try:
    next_page_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//li[@class='andes-pagination__button']/a[@aria-label='Ir a la página 2']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
    time.sleep(2)  

    next_page_button.click()
    time.sleep(5)

    search_results = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ui-search-results"))
    )
    
    product_cards = driver.find_elements(By.CLASS_NAME, "andes-card")

    for card in product_cards:
        try:
            title = card.find_element(By.CLASS_NAME, "ui-search-item__title").text
        except:
            title = "No disponible"
        
        try:
            price = card.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
        except:
            price = "No disponible"
        
        if title != "No disponible" and price != "No disponible":
            all_data.append([title, price])

except Exception as e:
    print(f"No se encontró el enlace a la siguiente página o hubo un error al hacer clic: {e}")

df = pd.DataFrame(all_data, columns=["Título", "Precio"])

df.to_excel("productos.xlsx", index=False)

driver.quit()