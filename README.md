# Cookie Inspector con FastAPI y Playwright

Este proyecto es una aplicación web construida con FastAPI que permite a los usuarios ingresar una URL y obtener una lista de las cookies utilizadas por ese sitio web. Además, enriquece esta información con detalles adicionales sobre cada cookie, como su descripción, categoría y periodo de retención, utilizando la base de datos Open Cookie Database.

## Funcionalidades

* **Obtención de Cookies:** Permite ingresar una URL y utiliza Playwright para navegar por el sitio y extraer sus cookies.
* **Enriquecimiento de Datos:** Cruza la información de las cookies obtenidas con la base de datos Open Cookie Database para proporcionar detalles adicionales.
* **Interfaz de Usuario:** Ofrece una interfaz web sencilla para ingresar la URL y visualizar los resultados.
* **API Backend:** Construido con FastAPI, proporcionando un backend robusto y eficiente.
* **CORS Habilitado:** Permite peticiones desde cualquier origen.

## Tecnologías Utilizadas

* **FastAPI:** Framework web moderno y de alto rendimiento para construir APIs con Python.
* **Playwright:** Biblioteca de Microsoft para automatizar navegadores Chromium, Firefox y WebKit.
* **Pydantic:** Biblioteca para la validación de datos y la configuración utilizando anotaciones de tipo Python.
* **Pandas:** Biblioteca para el análisis y manipulación de datos (utilizada para leer el CSV).
* **httpx:** Cliente HTTP asíncrono para realizar peticiones HTTP.
* **aiofiles:** Biblioteca para operaciones de archivos asíncronas.

## Requisitos

Asegúrate de tener Python 3.7+ instalado en tu sistema.

## Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    .\venv\Scripts\activate  # En Windows
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    Si no existe el archivo `requirements.txt`, puedes crearlo con las siguientes dependencias:
    ```
    fastapi
    uvicorn[standard]
    python-multipart
    fastapi[all]
    playwright
    pandas
    httpx
    aiofiles
    ```
    Después de crear el archivo, ejecuta el comando `pip install -r requirements.txt`.

4.  **Descarga los drivers de Playwright:**
    ```bash
    playwright install
    ```

## Configuración

* La base de datos de cookies (`open-cookie-database.csv`) se descarga automáticamente desde el repositorio de GitHub la primera vez que se ejecuta la aplicación o si el archivo no existe localmente en el directorio `datos`.
* El directorio para los datos se define como `datos`.
* La interfaz web (`index.html`) se encuentra en el directorio `static`.

## Ejecución

1.  **Ejecuta la aplicación FastAPI:**
    ```bash
    uvicorn main:app --reload
    ```
    Reemplaza `main` con el nombre de tu archivo principal de Python (si es diferente). La opción `--reload` permite que el servidor se reinicie automáticamente al detectar cambios en el código.

2.  **Accede a la aplicación en tu navegador:**
    Ve a `http://127.0.0.1:8000` en tu navegador para ver la interfaz web.

## Uso

1.  En la página principal, encontrarás un formulario donde puedes ingresar la URL del sitio web del que deseas inspeccionar las cookies.
2.  Introduce la URL en el campo proporcionado y haz clic en el botón "Obtener Cookies".
3.  La aplicación procesará la URL, obtendrá las cookies y mostrará una tabla con la información de cada cookie, incluyendo los detalles enriquecidos de la Open Cookie Database (si se encuentran).

## Estructura del Proyecto

.
├── datos/
│   └── open-cookie-database.csv  # Base de datos de cookies (se descarga automáticamente)
├── static/
│   └── index.html                # Interfaz web del usuario
├── main.py                       # Archivo principal de la aplicación FastAPI
├── requirements.txt              # Lista de dependencias del proyecto
└── README.md                     # Este archivo


## Logging

La aplicación utiliza el módulo `logging` de Python para registrar información relevante, como errores al leer el archivo CSV o al obtener las cookies. Los logs se mostrarán en la consola.

## Notas Adicionales

* Asegúrate de tener una conexión a internet activa la primera vez que ejecutes la aplicación para que se pueda descargar la base de datos de cookies.
* El rendimiento de la obtención de cookies puede variar dependiendo de la complejidad del sitio web y la velocidad de la conexión.
* La precisión de la información enriquecida depende de la disponibilidad de los datos en la Open Cookie Database.

# cookies_fastapi
