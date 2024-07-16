from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Edge()

try:
    driver.get("https://store.steampowered.com/")
    
    time.sleep(5)

    noteworthy_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "noteworthy_tab"))
    )
    noteworthy_tab.click()
    time.sleep(5)  

    popup_body = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "popup_body"))
    )

    popup_menu_browse = WebDriverWait(popup_body, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "popup_menu_browse"))
    )

 
    link_element = WebDriverWait(popup_menu_browse, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='popup_menu_item']"))
    )
    link_element.click()
    time.sleep(5)  


except Exception as e:
    print(f"Error: {e}")

finally:
  
    driver.quit()
