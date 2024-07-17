from seleniummethods import SeleniumWrapper
from excelexport import ExcelExporter
from selenium.webdriver.common.by import By  

def main():
    url = "https://www.meteored.mx/clima_Torreon-America+Norte-Mexico-Coahuila-MMTC-1-22375.html"
    output_file = "Clima.xlsx"

    scraper = SeleniumWrapper()
    excel_exporter = ExcelExporter(output_file)
    

    excel_exporter.set_columns(["Dia", "TempMinima", "TempMaxima", "ProbabilidadDeLluvia"])

    try:
        scraper.open_url(url)

        div_element = scraper.find_element(By.CLASS_NAME, "flex-r.dos-semanas.noche-nuevo")
        scraper.execute_script("arguments[0].scrollIntoView(true);", div_element)
        
        days = scraper.find_elements(By.XPATH, "//li[contains(@class, 'grid-item dia')]")
        for day in days:
            try:
                dia = day.find_element(By.CLASS_NAME, "subtitle-m").text
            except:
                dia = "No disponible"
            
            try:
                temp_minima = day.find_element(By.CLASS_NAME, "min.changeUnitT").text
            except:
                temp_minima = "No disponible"
            
            try:
                temp_maxima = day.find_element(By.CLASS_NAME, "max.changeUnitT").text
            except:
                temp_maxima = "No disponible"
            
            try:
                prob_lluvia = day.find_element(By.CLASS_NAME, "txt-strng.probabilidad.center").text
            except:
                prob_lluvia = "No disponible"
            
            if dia != "No disponible" and temp_minima != "No disponible" and temp_maxima != "No disponible" and prob_lluvia != "No disponible":
                excel_exporter.add_row([dia, temp_minima, temp_maxima, prob_lluvia])

        excel_exporter.export_to_excel()
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    main()
