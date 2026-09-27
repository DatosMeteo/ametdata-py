"""
Descarga respuestas reales de los endpoints de AEMET usados en los bloques A/B/C/E/F
y las guarda en subcarpetas dentro de EjemplossApi/ para poder ajustar el parseo
defensivo del frontend/backend con datos reales (en vez de asumir la estructura).

Ejecutar:
    python descargar_ejemplos.py
"""

import os
import re
import csv
import io
import json
import time
import urllib.parse
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _leer_api_key() -> str:
    """Lee una API key de AEMET desde AEMET-Api-download/config.py (texto, sin ejecutar imports)."""
    config_path = os.path.join(BASE_DIR, "..", "AEMET-Api-download", "config.py")
    with open(config_path, "r", encoding="utf-8") as f:
        texto = f.read()
    m = re.search(r'API_KEYS\s*=\s*\[(.*?)\]', texto, re.DOTALL)
    if not m:
        raise RuntimeError("No se encontraron API_KEYS en config.py")
    claves = re.findall(r'"([^"]+)"', m.group(1))
    if not claves:
        raise RuntimeError("Lista de API_KEYS vacía")
    return claves[0]


API_KEY = _leer_api_key()


def _guardar(subcarpeta: str, nombre: str, contenido):
    carpeta = os.path.join(BASE_DIR, subcarpeta)
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre)
    if isinstance(contenido, (dict, list)):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(contenido, f, ensure_ascii=False, indent=2)
    else:
        modo = "wb" if isinstance(contenido, bytes) else "w"
        with open(ruta, modo) as f:
            f.write(contenido)
    print(f"  -> guardado {ruta}")


def descargar_endpoint(path: str, subcarpeta: str, nombre_archivo: str, params: str = ""):
    """Descarga un endpoint AEMET (patrón meta->datos) y guarda meta + datos."""
    url = f"https://opendata.aemet.es/opendata/api{path}{params}?api_key={API_KEY}"
    print(f"GET {path}")
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        meta = resp.json()
        _guardar(subcarpeta, nombre_archivo.replace(".json", "_meta.json"), meta)

        datos_url = meta.get("datos")
        if not datos_url:
            print(f"  ❌ Sin 'datos' en meta: {meta}")
            return None

        resp2 = requests.get(datos_url, timeout=20)
        resp2.raise_for_status()
        try:
            datos = resp2.json()
            _guardar(subcarpeta, nombre_archivo, datos)
            return datos
        except Exception:
            # Puede no ser JSON (texto plano, etc.)
            _guardar(subcarpeta, nombre_archivo.replace(".json", ".txt"), resp2.text)
            return resp2.text

    except Exception as e:
        print(f"  ❌ Error en {path}: {e}")
        return None


def descargar_maestro_playas():
    print("GET maestro playas (CSV)")
    url = "https://www.aemet.es/documentos/es/eltiempo/prediccion/playas/Playas_codigos.csv"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        try:
            texto = resp.content.decode("utf-8")
        except UnicodeDecodeError:
            texto = resp.content.decode("latin-1")

        _guardar("playas", "maestro_playas_raw.csv", texto)

        sample = texto[:2000]
        try:
            delimiter = csv.Sniffer().sniff(sample, delimiters=";,").delimiter
        except Exception:
            delimiter = ";"

        reader = csv.reader(io.StringIO(texto), delimiter=delimiter)
        filas = [f for f in reader if f]
        print(f"  Delimitador detectado: '{delimiter}' | Cabeceras: {filas[0] if filas else 'N/A'}")
        _guardar("playas", "maestro_playas_headers.json", {"delimiter": delimiter, "headers": filas[0] if filas else [], "primera_fila_datos": filas[1] if len(filas) > 1 else []})

        return filas
    except Exception as e:
        print(f"  ❌ Error descargando maestro playas: {e}")
        return []


def main():
    # ── Bloque A: predicciones de texto ──────────────────────────────
    descargar_endpoint("/prediccion/nacional/hoy", "prediccion_nacional", "hoy.json")
    descargar_endpoint("/prediccion/ccaa/hoy/mad", "prediccion_ccaa", "mad_hoy.json")
    descargar_endpoint("/prediccion/provincia/hoy/28", "prediccion_provincia", "28_hoy.json")

    # ── Bloque B: UVI, montaña, nivológica ───────────────────────────
    descargar_endpoint("/prediccion/especifica/uvi/0", "uvi", "dia0.json")
    descargar_endpoint(
        f"/prediccion/especifica/{urllib.parse.quote('montaña')}/pasada/area/nev1/dia/0",
        "montana", "nev1_dia0.json"
    )
    descargar_endpoint("/prediccion/especifica/nivologica/0", "nivologica", "area0.json")

    # ── Bloque C: marítima ────────────────────────────────────────────
    descargar_endpoint("/prediccion/maritima/altamar/area/2", "maritima", "altamar_2.json")
    descargar_endpoint("/prediccion/maritima/costera/costa/45", "maritima", "costera_45.json")

    # ── Bloque E: redes especiales ────────────────────────────────────
    descargar_endpoint("/red/especial/ozono", "redes_especiales", "ozono.json")
    descargar_endpoint("/red/especial/radiacion", "redes_especiales", "radiacion.json")

    # ── Bloque B: playas (maestro + ejemplo) ──────────────────────────
    filas = descargar_maestro_playas()
    if len(filas) > 1:
        # Probar con el primer código de playa real del CSV
        primera_fila = filas[1]
        print(f"  Primera fila de playas (raw): {primera_fila}")
        # Heurística: probamos cada valor de la fila como posible código
        for valor in primera_fila:
            if valor and valor.strip().isdigit():
                codigo_playa = valor.strip()
                print(f"  Probando código de playa candidato: {codigo_playa}")
                resultado = descargar_endpoint(f"/prediccion/especifica/playa/{codigo_playa}", "playas", f"ejemplo_{codigo_playa}.json")
                if resultado:
                    break
                time.sleep(1)

    print("\n✅ Descarga de ejemplos completada. Revisa las subcarpetas en EjemplossApi/")


if __name__ == "__main__":
    main()
