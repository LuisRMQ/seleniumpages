from seleniummethods import SeleniumWrapper
from excelexport import ExcelExporter
from selenium.webdriver.common.by import By  

def main():
    url = "https://www.mercadolibre.com.mx/"
    output_file = "productos.xlsx"

    scraper = SeleniumWrapper()
    excel_exporter = ExcelExporter(output_file)
    all_data = []

    excel_exporter.set_columns(["Título", "Precio"])

    try:
        scraper.open_url(url)

        input_element = scraper.find_element(By.ID, "cb1-edit")
        scraper.send_keys(input_element, "Computadora")

        submit_button = scraper.find_element(By.CLASS_NAME, "nav-icon-search")
        scraper.click(submit_button)

        search_results = scraper.wait_for_element(By.CLASS_NAME, "ui-search-results")

        product_cards = scraper.find_elements(By.CLASS_NAME, "andes-card")

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
                excel_exporter.add_row([title, price])

        try:
            next_page_button = scraper.wait_for_element(
                By.XPATH, "//li[@class='andes-pagination__button']/a[@aria-label='Ir a la página 2']"
            )
            scraper.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
            scraper.click(next_page_button)

            search_results = scraper.wait_for_element(By.CLASS_NAME, "ui-search-results")
            product_cards = scraper.find_elements(By.CLASS_NAME, "andes-card")

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
                    excel_exporter.add_row([title, price])

        except Exception as e:
            print(f"No se encontró el enlace a la siguiente página o hubo un error al hacer clic: {e}")

        excel_exporter.export_to_excel()
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    main()
