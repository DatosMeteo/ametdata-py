"""
Compara la fecha del texto en Firebase vs lo que devuelve AEMET AHORA MISMO
para determinar si Firebase está desactualizado o si AEMET genuinamente da
textos con fechas viejas (su comportamiento por defecto es devolver el último
elaborado aunque sea de hace días).
"""
import os
import re
import time
import requests
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _leer_api_key():
    config_path = os.path.join(BASE_DIR, "..", "AEMET-Api-download", "config.py")
    with open(config_path, "r", encoding="utf-8") as f:
        texto = f.read()
    m = re.search(r'API_KEYS\s*=\s*\[(.*?)\]', texto, re.DOTALL)
    claves = re.findall(r'"([^"]+)"', m.group(1)) if m else []
    return claves[0] if claves else None

API_KEY = _leer_api_key()
BASE_URL = "https://opendata.aemet.es/opendata/api"

# Solo verificar un subconjunto para no saturar AEMET
CCAA_MUESTRA = ["and", "arn", "val", "nav", "mad", "cle"]

patron_fecha = re.compile(
    r"D[ÍI]A\s+(\d+)\s+DE\s+(\w+)\s+DE\s+(\d{4})",
    re.IGNORECASE
)
MESES = {
    "enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,
    "julio":7,"agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12
}

def extraer_fecha(texto):
    m = patron_fecha.search(texto)
    if not m:
        return None
    dia, mes_str, anio = int(m.group(1)), m.group(2).lower(), int(m.group(3))
    mes = MESES.get(mes_str)
    if mes:
        return datetime(anio, mes, dia, tzinfo=timezone.utc).date()
    return None

def fecha_aemet_vivo(ccaa):
    try:
        url = f"{BASE_URL}/prediccion/ccaa/hoy/{ccaa}?api_key={API_KEY}"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        meta = r.json()
        datos_url = meta.get("datos")
        if not datos_url:
            return None
        r2 = requests.get(datos_url, timeout=15)
        r2.raise_for_status()
        try:
            texto = r2.content.decode("utf-8")
        except UnicodeDecodeError:
            texto = r2.content.decode("latin-1")
        return extraer_fecha(texto)
    except Exception as e:
        return f"ERROR: {e}"

hoy = datetime.now(timezone.utc).date()
print(f"Fecha actual: {hoy}\n")
print(f"{'CCAA':<6} {'En Firebase':<14} {'AEMET en vivo':<14} {'Diagnóstico'}")
print("-" * 65)

import firebase_admin
from firebase_admin import credentials, db as firebase_db

CRED_FILE = os.path.join(BASE_DIR, "..", "Firebase-Acces", "datosmeteo-a2251-firebase-adminsdk-fbsvc-2f03734ac0.json")
cred = credentials.Certificate(CRED_FILE)
firebase_admin.initialize_app(cred, {"databaseURL": "https://datosmeteo-a2251-default-rtdb.europe-west1.firebasedatabase.app/"})

for ccaa in CCAA_MUESTRA:
    datos_fb = firebase_db.reference(f"/prediccionTexto/ccaa/{ccaa}/hoy").get()
    fecha_fb = extraer_fecha(str(datos_fb or ""))

    fecha_live = fecha_aemet_vivo(ccaa)
    time.sleep(1)  # evitar rate-limit

    if isinstance(fecha_live, str) and fecha_live.startswith("ERROR"):
        diagn = "AEMET falla"
    elif fecha_live is None:
        diagn = "AEMET sin fecha"
    elif fecha_fb == fecha_live:
        if fecha_fb == hoy:
            diagn = "OK - HOY"
        else:
            lag = (hoy - fecha_fb).days
            diagn = f"Ambos {lag}d viejos (AEMET no ha actualizado)"
    else:
        diagn = "DESINCRONIZADO (Firebase mas viejo que AEMET)"

    fecha_fb_str = str(fecha_fb) if fecha_fb else "AUSENTE"
    fecha_live_str = str(fecha_live) if fecha_live else "—"
    print(f"{ccaa:<6} {fecha_fb_str:<14} {fecha_live_str:<14} {diagn}")
