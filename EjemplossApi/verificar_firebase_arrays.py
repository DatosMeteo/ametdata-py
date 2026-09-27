"""
Diagnóstico: comprueba si Firebase RTDB devuelve los arrays guardados desde Python
(listas) como arrays JSON reales o como objetos con claves "0","1",... al leerlos
de vuelta. Esto determina si el frontend necesita normalizar la respuesta.
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(BASE_DIR, "..", "Firebase-Acces", "datosmeteo-a2251-firebase-adminsdk-fbsvc-2f03734ac0.json")
DB_URL = "https://datosmeteo-a2251-default-rtdb.europe-west1.firebasedatabase.app/"

cred = credentials.Certificate(CRED_FILE)
firebase_admin.initialize_app(cred, {"databaseURL": DB_URL})

RUTAS = [
    "/prediccionTexto/ccaa/and/hoy",
    "/prediccionTexto/ccaa/bal/hoy",
    "/prediccionTexto/ccaa/cle/hoy",
    "/prediccionTexto/ccaa/mad/hoy",
    "/prediccionTexto/ccaa/cat/hoy",
    "/prediccionTexto/ccaa/and_ultima_actualizacion",
]

for ruta in RUTAS:
    datos = db.reference(ruta).get()
    tipo = type(datos).__name__
    print(f"\n=== {ruta} === tipo Python: {tipo}")
    if isinstance(datos, dict):
        claves = list(datos.keys())[:5]
        print(f"  Es DICT. Primeras claves: {claves}")
        print(f"  ¿Claves numéricas secuenciales (array roto)?: {all(k.isdigit() for k in claves[:5])}")
    elif isinstance(datos, list):
        print(f"  Es LIST de longitud {len(datos)}. Primer elemento (tipo): {type(datos[0]).__name__ if datos else 'N/A'}")
    else:
        print(f"  Valor: {str(datos)[:200]}")

    # Volcar un fragmento legible
    try:
        print("  JSON (primeros 500 chars):", json.dumps(datos, ensure_ascii=False)[:500])
    except Exception as e:
        print("  No serializable:", e)

print("\n\n=== Todas las claves bajo /prediccionTexto/ccaa ===")
todas = db.reference("/prediccionTexto/ccaa").get()
if isinstance(todas, dict):
    for ccaa_key, plazos in todas.items():
        if isinstance(plazos, dict):
            print(f"  {ccaa_key}: plazos disponibles = {list(plazos.keys())}")
        else:
            print(f"  {ccaa_key}: {type(plazos).__name__} -> {str(plazos)[:100]}")
else:
    print("  (vacío o no es dict):", todas)
