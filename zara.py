from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import argparse
from time import sleep

# Función para configurar el navegador y aceptar cookies
def setup_browser(url):
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 150) #ponemos un tiempo de espera de 150 segundos como máximo
    
    driver.get(url) #abrimos la url

    # Hacer click en el botón de aceptar cookies
    element = wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
    element.click()

    return driver, wait

# Función para obtener las URLs de los productos
def get_product_urls(driver, wait):
    product_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-link")))
    product_urls = set()  # Usamos un set para evitar duplicados
    for element in product_elements:
        product_url = element.get_attribute("href") # Obtener la URL del producto
        if product_url not in product_urls:
            product_urls.add(product_url) # pese a que es un set, controlamos que no se repitan las urls para evitar fallos debido a la gran cantidad de datos

    return list(product_urls)

# Función para procesar un producto y obtener las tallas y/o colores
def process_product(driver, wait, product_url):
    driver.get(product_url)

    available_sizes, low_stock_sizes, out_of_stock_sizes, scraped_data = [], [], [], [] 
    product_name = driver.find_element(By.CLASS_NAME, "product-detail-info__header-name").text

    # Verificar si hay tallas
    size_elements = driver.find_elements(By.CLASS_NAME, "size-selector__size-list-item")
    if size_elements:
        available_sizes, low_stock_sizes, out_of_stock_sizes = process_sizes(size_elements)

    # Verificar si hay colores
    color_elements = driver.find_elements(By.CLASS_NAME, "product-detail-color-selector__color")
    if color_elements:
        for color_element in color_elements:
            # Hacer clic en el color
            color_element.click()
            sleep(3)  # Espera un momento para que se actualicen las tallas

            # Obtener las tallas para este color
            sizes_for_color = driver.find_elements(By.CLASS_NAME, "size-selector__size-list-item")
            if sizes_for_color:
                color = color_element.find_element(By.CLASS_NAME, "screen-reader-text")
                sizes_available, low_stock_sizes, out_of_stock_sizes = process_sizes(sizes_for_color)
                scraped_data.append({
                    "Producto: ": product_name,
                    "Color": color.get_attribute("innerText"),
                    "Tallas disponibles": sizes_available,
                    "Tallas con poco stock": low_stock_sizes,
                    "Tallas sin stock": out_of_stock_sizes,
                    "URL": product_url
                })

    return available_sizes, low_stock_sizes, out_of_stock_sizes, scraped_data


def process_sizes(size_elements):
    available_sizes = []
    low_stock_sizes = []
    out_of_stock_sizes = []

    sleep(1)
    for size_element in size_elements:
        size_text = size_element.find_element(By.CLASS_NAME, "product-size-info__main-label").text

        # Buscar el elemento que indica la disponibilidad
        try:
            availability_hint_element = size_element.find_element(By.CLASS_NAME, "product-size-info__second-line")

            # Obtener el texto de la disponibilidad
            availability_text = availability_hint_element.text

            if "POCAS UNIDADES" in availability_text:
                low_stock_sizes.append(size_text)
            elif "COMING SOON" in availability_text or "VER SIMILARES" in availability_text:
                out_of_stock_sizes.append(size_text)
            else:
                available_sizes.append(size_text)

        except NoSuchElementException:
            # Si no se encuentra el elemento, la talla está disponible
            available_sizes.append(size_text)

    return available_sizes, low_stock_sizes, out_of_stock_sizes


# Función para procesar colores
def process_colors(color_elements):
    available_colors = []

    for color_element in color_elements:
        element = color_element.find_element(By.CLASS_NAME, "screen-reader-text")
        color_name = element.get_attribute("innerText")
        available_colors.append(color_name)

    return available_colors

# Función principal
import pandas as pd
# ... (tu código anterior)

def main():
    parser = argparse.ArgumentParser(description="Web scraping de productos Zara")
    parser.add_argument("-v", "--verbose", action="store_true", help="Imprimir información detallada")
    parser.add_argument("-i", "--individual", action="store_true", help="Guardar en archivos CSV individuales")
    parser.add_argument("-c", "--cantidad", type=int, help="Número de productos a raspar")
    args = parser.parse_args()

    url = "https://www.zara.com/es/es/mujer-precios-especiales-l1314.html?v1=2291858"
    driver, wait = setup_browser(url)
    product_urls = get_product_urls(driver, wait)

    all_products = []  # Lista para almacenar todos los productos

    for product_url in product_urls[:args.cantidad] if args.cantidad else product_urls:
        result = process_product(driver, wait, product_url)
        product_name = driver.find_element(By.CLASS_NAME, "product-detail-info__header-name").text

        if result:
            available_sizes, low_stock_sizes, out_of_stock_sizes, scraped_data = result

            if scraped_data:
                for data in scraped_data:
                    if args.verbose:
                        print(f"Guardando datos de {product_name} en CSV individual.")
                    product_df = pd.DataFrame([data])
                    product_df.to_csv(f"Data/{product_name}_{data['Color']}.csv", index=False)
            else:
                product_data = {
                    "Producto": product_name,
                    "Colores disponibles": "Color único",
                    "Tallas disponibles": available_sizes,
                    "Tallas con poco stock": low_stock_sizes,
                    "Tallas sin stock": out_of_stock_sizes,
                    "URL": product_url
                }
                all_products.append(product_data)
                if args.verbose:
                    print(f"Añadiendo datos de {product_name} al archivo CSV general.")

    driver.quit()

    if not args.individual:
        if args.verbose:
            print("Guardando todos los datos en un solo archivo CSV.")
        df = pd.DataFrame(all_products)
        df.to_csv("Data/productos_zara.csv", index=False)  # Guardar los datos en un solo archivo CSV

if __name__ == "__main__":
    main()
