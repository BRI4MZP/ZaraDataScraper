<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Web Scraping de Productos Zara: Automatiza la recopilación de datos de productos de Zara utilizando Python y Selenium.">
    <meta name="keywords" content="web scraping, Zara, Python, Selenium, productos, datos, scraping, programación">
    <title>Web Scraping de Productos Zara</title>
</head>
<body>
    <header>
        <h1>Web Scraping de Productos Zara</h1>
        <p>Automatiza la recopilación de datos de productos de Zara utilizando Python y Selenium.</p>
    </header>

    <section>
        <h2>Requisitos Previos</h2>
        <p>Asegúrese de tener instaladas las siguientes bibliotecas de Python:</p>
        <ul>
            <li><code>selenium</code>: Para la automatización del navegador.</li>
            <li><code>pandas</code>: Para la manipulación y almacenamiento de datos en formato CSV.</li>
            <li><code>argparse</code>: Para el manejo de argumentos de línea de comandos.</li>
        </ul>
        <p>Puede instalar estas bibliotecas utilizando <code>pip</code>:</p>
        <pre><code>pip install selenium pandas</code></pre>
    </section>

    <section>
        <h2>Uso del Programa</h2>
        <p>El programa ofrece varias opciones de línea de comandos:</p>
        <ul>
            <li><code>-v</code> o <code>--verbose</code>: Imprimir información detallada durante la ejecución.</li>
            <li><code>-i</code> o <code>--individual</code>: Guardar los datos de cada producto en archivos CSV individuales.</li>
            <li><code>-c</code> o <code>--cantidad</code>: Especificar el número de productos a raspar. Si no se proporciona, se recopilarán todos los productos en la página.</li>
        </ul>
        <p>Para ejecutar el programa, simplemente ejecute el script Python desde la línea de comandos:</p>
        <pre><code>python nombre_del_programa.py</code></pre>
        <p>Ejemplo de uso con argumentos:</p>
        <pre><code>python nombre_del_programa.py -v -i -c 10</code></pre>
    </section>

    <section>
        <h2>Funcionamiento del Programa</h2>
        <p>El programa sigue los siguientes pasos:</p>
        <ol>
            <li>Abre una instancia del navegador Firefox y navega a la URL proporcionada.</li>
            <li>Acepta las cookies haciendo clic en el botón correspondiente.</li>
            <li>Recopila las URL de los productos disponibles en la página.</li>
            <li>Procesa cada URL de producto para obtener información sobre tallas, colores y disponibilidad.</li>
            <li>Almacena los datos recopilados en archivos CSV, ya sea en archivos individuales por producto o en un archivo CSV general.</li>
        </ol>
    </section>

    <section>
        <h2>Resultados</h2>
        <p>El programa almacena los datos recopilados en archivos CSV, que pueden ser útiles para el análisis posterior. Puede elegir entre guardar los datos en archivos individuales por producto o en un solo archivo CSV general, según sus necesidades.</p>
    </section>

    <section>
        <h2>Aviso Legal</h2>
        <p>Este programa se proporciona solo con fines educativos y de demostración. El scraping de sitios web puede tener implicaciones legales y éticas, y es importante respetar los términos de servicio del sitio web que está raspando. El uso de este programa debe cumplir con todas las leyes y regulaciones aplicables.</p>
    </section>

    <section>
        <h2>Autor</h2>
        <p>Este programa fue desarrollado por [Su Nombre].</p>
        <p>¡Esperamos que encuentre útil este programa para su análisis de productos en el sitio web de Zara! Si tiene alguna pregunta o comentario, no dude en ponerse en contacto con nosotros.</p>
    </section>
</body>
</html>
