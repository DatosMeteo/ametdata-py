import sys
import os
import csv
import io
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "AEMET-Api-download", "services"))


def _dms_a_decimal(valor):
    if not valor:
        return None
    texto = valor.strip()
    negativo = texto.startswith("-")
    texto = texto.lstrip("-").replace('"', "")
    m = re.match(r"(\d+)\s*[ºo°]\s*(\d+)\s*['\s]+(\d+(?:[.,]\d+)?)", texto)
    if not m:
        return None
    grados, minutos, segundos = m.groups()
    decimal = float(grados) + float(minutos) / 60 + float(segundos.replace(",", ".")) / 3600
    return -decimal if negativo else decimal


def _detectar_columna_exacta(headers, nombres_exactos):
    headers_norm = [(h or "").strip().upper() for h in headers]
    for nombre in nombres_exactos:
        if nombre in headers_norm:
            return headers_norm.index(nombre)
    return None


# Test DMS
print("=== Test DMS ===")
print("38º 34' 31\" ->", _dms_a_decimal("38º 34' 31\""))
print("-00º 03' 52\" ->", _dms_a_decimal("-00º 03' 52\""))

# Test columna detection con headers reales
headers = ["ID_PLAYA", "NOMBRE_PLAYA", "ID_PROVINCIA", "NOMBRE_PROVINCIA", "ID_MUNICIPIO", "NOMBRE_MUNICIPIO", "LATITUD", "LONGITUD"]
print("\n=== Test deteccion columnas ===")
print("idx_codigo (ID_PLAYA):", _detectar_columna_exacta(headers, ["ID_PLAYA"]))
print("idx_nombre (NOMBRE_PLAYA):", _detectar_columna_exacta(headers, ["NOMBRE_PLAYA"]))
print("idx_municipio (NOMBRE_MUNICIPIO):", _detectar_columna_exacta(headers, ["NOMBRE_MUNICIPIO"]))
print("idx_provincia (NOMBRE_PROVINCIA):", _detectar_columna_exacta(headers, ["NOMBRE_PROVINCIA"]))
print("idx_lat (LATITUD):", _detectar_columna_exacta(headers, ["LATITUD", "LAT"]))
print("idx_lon (LONGITUD):", _detectar_columna_exacta(headers, ["LONGITUD", "LON"]))

# Test con el CSV real completo
# Nota: el archivo de ejemplo se guardó sin encoding explícito (open() por defecto
# usa cp1252 en Windows); el backend real nunca escribe a disco, parsea en memoria.
print("\n=== Test con CSV real (primeras 5 playas) ===")
csv_path = os.path.join(os.path.dirname(__file__), "playas", "maestro_playas_raw.csv")
try:
    with open(csv_path, "r", encoding="utf-8") as f:
        texto = f.read()
except UnicodeDecodeError:
    with open(csv_path, "r", encoding="cp1252") as f:
        texto = f.read()

reader = csv.reader(io.StringIO(texto), delimiter=";")
filas = [f for f in reader if f]
headers_reales = filas[0]
idx_codigo = _detectar_columna_exacta(headers_reales, ["ID_PLAYA"])
idx_nombre = _detectar_columna_exacta(headers_reales, ["NOMBRE_PLAYA"])
idx_lat = _detectar_columna_exacta(headers_reales, ["LATITUD", "LAT"])
idx_lon = _detectar_columna_exacta(headers_reales, ["LONGITUD", "LON"])

for fila in filas[1:6]:
    codigo = fila[idx_codigo] if idx_codigo is not None else None
    nombre = fila[idx_nombre] if idx_nombre is not None else None
    lat_raw = fila[idx_lat] if idx_lat is not None else None
    lon_raw = fila[idx_lon] if idx_lon is not None else None
    lat = _dms_a_decimal(lat_raw)
    lon = _dms_a_decimal(lon_raw)
    print(f"{codigo} | {nombre} | lat_raw={lat_raw!r} -> {lat} | lon_raw={lon_raw!r} -> {lon}")

print(f"\nTotal playas en CSV: {len(filas) - 1}")

# Test parseo CSV de ozono
print("\n=== Test parseo ozono ===")


def _parsear_csv_aemet(texto):
    reader = list(csv.reader(io.StringIO(texto), delimiter=";"))
    reader = [f for f in reader if f]
    if len(reader) < 3:
        return {"titulo": None, "fecha": None, "headers": [], "filas": []}
    return {
        "titulo": reader[0][0] if reader[0] else None,
        "fecha": reader[1][0] if reader[1] else None,
        "headers": reader[2],
        "filas": reader[3:],
    }


try:
    with open(os.path.join(os.path.dirname(__file__), "redes_especiales", "ozono.txt"), "r", encoding="utf-8") as f:
        ozono_texto = f.read()
except UnicodeDecodeError:
    with open(os.path.join(os.path.dirname(__file__), "redes_especiales", "ozono.txt"), "r", encoding="cp1252") as f:
        ozono_texto = f.read()

resultado = _parsear_csv_aemet(ozono_texto)
print("Titulo:", resultado["titulo"])
print("Fecha:", resultado["fecha"])
print("Headers:", resultado["headers"])
print("Primeras 2 filas:", resultado["filas"][:2])
