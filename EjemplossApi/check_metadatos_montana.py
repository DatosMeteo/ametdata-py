import os, re, json, urllib.parse
import requests

BASE = os.path.dirname(os.path.abspath(__file__))

def _leer_api_key():
    config_path = os.path.join(BASE, "..", "AEMET-Api-download", "config.py")
    with open(config_path, "r", encoding="utf-8") as f:
        texto = f.read()
    m = re.search(r'API_KEYS\s*=\s*\[(.*?)\]', texto, re.DOTALL)
    claves = re.findall(r'"([^"]+)"', m.group(1)) if m else []
    return claves[0] if claves else None

API_KEY = _leer_api_key()
area = "nev1"
url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/{urllib.parse.quote('montaña')}/pasada/area/{area}/dia/0?api_key={API_KEY}"

r = requests.get(url, timeout=20)
r.raise_for_status()
meta = r.json()
print("META:", json.dumps(meta, indent=2, ensure_ascii=False))

# Descargar datos
r2 = requests.get(meta["datos"], timeout=20)
r2.raise_for_status()
print("\n=== DATOS (completo) ===")
try:
    datos = r2.json()
    print(json.dumps(datos, indent=2, ensure_ascii=False))
except Exception:
    print(r2.content.decode("latin-1"))

# Descargar metadatos (esquema/descripción del producto)
if "metadatos" in meta:
    r3 = requests.get(meta["metadatos"], timeout=20)
    r3.raise_for_status()
    print("\n=== METADATOS ===")
    try:
        md = r3.json()
        print(json.dumps(md, indent=2, ensure_ascii=False)[:3000])
    except Exception:
        print(r3.content.decode("latin-1")[:3000])
