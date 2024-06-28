from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import pandas as pd
import argparse
from time import sleep

# Función para configurar el navegador y aceptar cookies
def setup_browser(url, arg):
    options = Options() 
    options.add_argument("-headless") 
    if arg.window:
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 20) #ponemos un tiempo de espera de 10 segundos como máximo

	# Abrir la página
    driver.get(url)
    
	# gestión de errores para cookies
    try:
        wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
    except:
        pass
    
    return driver, wait

# Función para obtener las URLs de los productos
def get_product_urls(driver, wait):
    # array de productos en la página. Creamos un set para las urls y evitar duplicados
    product_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-link")))
    product_urls = set()

	# Iteramos los elementos de la página y obtenemos las urls de los productos
    for element in product_elements:
        product_url = element.get_attribute("href") # Obtener la URL del producto
        if product_url not in product_urls:
            product_urls.add(product_url) # pese a que es un set, controlamos que no se repitan las urls para evitar fallos debido a la gran cantidad de datos

    return list(product_urls)

# Función para procesar un producto y obtener las tallas y/o colores
def process_product(driver, wait, product_url):
    driver.get(product_url)

	# Inicializar las listas de tallas y colores
    available_sizes, low_stock_sizes, out_of_stock_sizes, scraped_data = [], [], [], [] 
    
	# Obtener el nombre del producto
    product_name = driver.find_element(By.CLASS_NAME, "product-detail-info__header-name").text

    # Verificar si hay tallas y las procesamos en la función process_sizes.
    size_elements = driver.find_elements(By.CLASS_NAME, "size-selector-list__item")
    if size_elements:
        available_sizes, low_stock_sizes, out_of_stock_sizes = process_sizes(size_elements)

    # Verificar si hay colores disponibles
    color_elements = driver.find_elements(By.CLASS_NAME, "product-detail-color-selector__color")
    if color_elements:
        # Iteramos los colores y accedemos a las tallas disponibles para cada color
        for color_element in color_elements:
            color_element.click()
            sleep(1)
            sizes_for_color = driver.find_elements(By.CLASS_NAME, "size-selector-list__item")
            # Si hay tallas disponibles para ese color, las procesamos 
            if sizes_for_color:
                color = color_element.find_element(By.CLASS_NAME, "screen-reader-text")
                price = driver.find_element(By.CLASS_NAME, "price-current__amount").text
                try:
                    discount = driver.find_element(By.CLASS_NAME, "price-current__discount-percentage").text
                except:
                    discount = "0%"
                sizes_available, low_stock_sizes, out_of_stock_sizes = process_sizes(sizes_for_color)
                # Guardamos los datos en un diccionario con todos los datos del producto
                scraped_data.append({
                    "Producto: ": product_name,
                    "Color": color.get_attribute("innerText"),
                    "Precio": price,
                    "Descuento": discount,
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

def main():
    # configuración de la libreía argparse para recibir argumentos
    parser = argparse.ArgumentParser(description="Web scraping de productos Zara")
    parser.add_argument("-v", "--verbose", action="store_true", help="Imprimir información detallada")
    parser.add_argument("-i", "--individual", action="store_true", help="Guardar en archivos CSV individuales")
    parser.add_argument("-c", "--cantidad", type=int, help="Número de productos a raspar")
    parser.add_argument("-w", "--window", action="store_true", help="Mostrar el navegador")
    args = parser.parse_args()

    # url = "https://www.zara.com/es/es/mujer-precios-especiales-l1314.html?v1=2291858"
    url = "https://www.zara.com/es/es/hombre-venta-l7139.html?v1=2439352"
    driver, wait = setup_browser(url, args)
    product_urls = get_product_urls(driver, wait)

    # iteramos sobre las urls de los productos y procesamos cada uno
    for product_url in product_urls[:args.cantidad] if args.cantidad else product_urls:

        # obtenemos los datos del producto
        result = process_product(driver, wait, product_url)
        product_name = driver.find_element(By.CLASS_NAME, "product-detail-info__header-name").text

        # si hay datos, los guardamos, si no, el programa continua
        if result:
            available_sizes, low_stock_sizes, out_of_stock_sizes, scraped_data = result

            # En este caso tratamos los productos que tengan varios colores disponibles
            if scraped_data:
                if args.individual:
                    if args.verbose:
                        print(f"Guardando datos de {product_name} en un archivo CSV individual.")
                    df = pd.DataFrame(scraped_data)
                    df.to_csv(f"Data/{product_name}.csv", mode="a", index=False, header=False)
                else:
                    if args.verbose:
                        print(f"Añadiendo datos de {product_name} al archivo CSV general.")
                    df = pd.DataFrame(scraped_data)
                    df.to_csv("Data/productos_zara.csv", mode="a", index=False, header=False)
            
            # En este caso tratamos los productos que tengan un solo color y obtenemos precio y descuento
            else:
                price = driver.find_element(By.CLASS_NAME, "price-current__amount").text
                try:
                    discount = driver.find_element(By.CLASS_NAME, "price-current__discount-percentage").text
                except:
                    discount = "0%"

                product_data = {
                    "Producto": product_name,
                    "Color": "Color único",
                    "Precio": price,
                    "Descuento": discount,
                    "Tallas disponibles": available_sizes,
                    "Tallas con poco stock": low_stock_sizes,
                    "Tallas sin stock": out_of_stock_sizes,
                    "URL": product_url
                }
                # Guardamos los datos en un archivo CSV individual o general
                if args.individual:
                    if args.verbose:
                        print(f"Guardando datos de {product_name} en un archivo CSV individual.")
                    df = pd.DataFrame([product_data])
                    df.to_csv(f"Data/{product_name}.csv",mode="a", index=False, header=False)
                else:
                    if args.verbose:
                        print(f"Añadiendo datos de {product_name} al archivo CSV general.")
                    df = pd.DataFrame([product_data])
                    df.to_csv("Data/productos_zara.csv", mode="a", index=False, header=False)
    driver.quit()

if __name__ == "__main__":
    main()
