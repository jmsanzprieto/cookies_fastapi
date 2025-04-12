from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from playwright.async_api import async_playwright
import pandas as pd
import os
import aiofiles
import httpx
import logging

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configura el directorio para archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

DATA_DIR = "datos"
CSV_FILE = os.path.join(DATA_DIR, "open-cookie-database.csv")
CSV_URL = "https://raw.githubusercontent.com/jkwakman/Open-Cookie-Database/master/open-cookie-database.csv"

class URLRequest(BaseModel):
    url: str

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Asegurarse de que el archivo CSV exista
async def ensure_csv_exists():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(CSV_FILE):
        async with httpx.AsyncClient() as client:
            response = await client.get(CSV_URL)
            if response.status_code == 200:
                async with aiofiles.open(CSV_FILE, "w", encoding="utf-8") as f:
                    await f.write(response.text)
            else:
                raise Exception("No se pudo descargar el archivo CSV.")

# Obtener cookies de una URL usando Playwright
async def get_cookies_from_url(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state('networkidle')
        cookies = await page.context.cookies()
        await browser.close()
        return cookies

# Enriquecer las cookies con información adicional
def enrich_cookies(cookies: list):
    try:
        df = pd.read_csv(CSV_FILE)
        df.columns = [col.strip() for col in df.columns]
    except Exception as e:
        logging.error(f"Error leyendo el CSV: {e}")
        return cookies

    enriched = []
    for cookie in cookies:
        name = cookie.get("name", "")
        match = df[df["Cookie / Data Key name"].str.strip().str.lower() == name.strip().lower()]
        if not match.empty:
            first_match = match.iloc[0]
            cookie["descripcion"] = first_match.get("Description", "")            
            cookie["categoria"] = first_match.get("Category", "")            
            cookie["retencion"] = first_match.get("Retention period", "")
           
        else:
            cookie["descripcion"] = ""
            cookie["categoria"] = ""
            cookie["retencion"] = ""
           
        enriched.append(cookie)
    return enriched

# Ruta principal para servir index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        # Sirve el archivo index.html desde el directorio estático
        with open("static/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        logging.error(f"Error al leer el archivo HTML: {e}")
        raise HTTPException(status_code=500, detail="Error al cargar la página")

# Ruta para manejar el formulario y obtener las cookies
@app.post("/get_cookies")
async def get_cookies(request: URLRequest):
    try:
        await ensure_csv_exists()
        cookies = await get_cookies_from_url(request.url)
        enriched_cookies = enrich_cookies(cookies)  # Enriquecer las cookies
        return {"cookies": enriched_cookies}  # Devolver la lista enriquecida
    except Exception as e:
        logging.error(f"Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener cookies: {e}")