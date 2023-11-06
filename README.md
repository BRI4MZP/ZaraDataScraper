# Web Scraping de Productos Zara

Automatiza la recopilación de datos de productos de Zara utilizando Python y Selenium.

## Requisitos Previos
Asegúrese de tener instaladas las siguientes bibliotecas de Python:

- `selenium`: Para la automatización del navegador.
- `pandas`: Para la manipulación y almacenamiento de datos en formato CSV.
- `argparse`: Para el manejo de argumentos de línea de comandos.

Puede instalar estas bibliotecas utilizando `pip` install -r requirements.txt:

## Uso del Programa

El programa ofrece varias opciones de línea de comandos:

- -v o --verbose: Imprimir información detallada durante la ejecución.
- -i o --individual: Guardar los datos de cada producto en archivos CSV individuales.
- -c o --cantidad: Especificar el número de productos que se quieren scrapear. Si no se proporciona, se recopilarán todos los productos en la página.
- -w o --window: Muestra el navegador en funcionamiento para ver la ejecución del programa.

## Ejemplos de uso

`python zara.py -v -i -w -c=10`

`python zara.py -v -w`

`python zara.py -c=10`

## Funcionamiento del Programa

El programa sigue los siguientes pasos:

- Abre una instancia del navegador Firefox y navega a la URL proporcionada.
- Acepta las cookies haciendo clic en el botón correspondiente.
- Recopila las URL de los productos disponibles en la página.
- Procesa cada URL de producto para obtener información sobre tallas, colores y disponibilidad.
- Almacena los datos recopilados en archivos CSV, ya sea en archivos individuales por producto o en un archivo CSV general.

## Resultados

El programa almacena los datos recopilados en archivos CSV, que pueden ser útiles para el análisis posterior. Puede elegir entre guardar los datos en archivos individuales por producto o en un solo archivo CSV general, según sus necesidades.

## Aviso Legal

Este programa se proporciona solo con fines educativos y de demostración. El scraping de sitios web puede tener implicaciones legales y éticas, y es importante respetar los términos de servicio del sitio web que está raspando. El uso de este programa debe cumplir con todas las leyes y regulaciones aplicables.

## Autor

Este programa fue desarrollado por BRI4MZP.

¡Espero que encuentre útil este programa para su análisis de productos en el sitio web de Zara! Si tiene alguna pregunta o comentario, no dude ponerse en contacto.
