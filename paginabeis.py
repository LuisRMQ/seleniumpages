from seleniummethods import SeleniumWrapper
from excelexport import ExcelExporter
from selenium.webdriver.common.by import By  
import time

def extract_and_export(scraper, excel_exporter):
    table_element = scraper.find_element(By.CLASS_NAME, "mini__toggled-table__container")
    scraper.execute_script("arguments[0].scrollIntoView(true);", table_element)
    
    tbody_element = table_element.find_element(By.TAG_NAME, "tbody")
    
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")
    
    for row in rows:
        row_data = []
        
        try:
            equipo = row.find_element(By.XPATH, ".//td[@data-col='0']").text
        except:
            equipo = "No disponible"
        row_data.append(equipo)
        
        for i in range(1, 5):
            try:
                col = row.find_element(By.XPATH, f".//td[@data-col='{i}']").text
            except:
                col = "No disponible"
            row_data.append(col)
        
        excel_exporter.add_row(row_data)

    excel_exporter.export_to_excel()

def main():
    url = "https://www.milb.com/mexican"
    output_file = "EstadisticasBeisbol_LigaNORTE.xlsx"

    scraper = SeleniumWrapper()
    excel_exporter_norte = ExcelExporter(output_file)
    
    excel_exporter_norte.set_columns(["Equipo", "Ganados", "Perdidos", "Porcentaje", "Diferencia"])
   
    try:
        scraper.open_url(url)
        time.sleep(10)
        
        try:
            accept_cookies_button = scraper.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']")
            accept_cookies_button.click()
            time.sleep(2)  
        except:
            pass 

        extract_and_export(scraper, excel_exporter_norte)
    
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    main()
