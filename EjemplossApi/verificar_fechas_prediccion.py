"""
Verifica qué fecha tienen las predicciones de texto almacenadas en Firebase
para cada CCAA bajo /prediccionTexto/ccaa/{ccaa}/hoy
"""
import os
import re
from datetime import datetime, timezone
import firebase_admin
from firebase_admin import credentials, db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(BASE_DIR, "..", "Firebase-Acces", "datosmeteo-a2251-firebase-adminsdk-fbsvc-2f03734ac0.json")
DB_URL = "https://datosmeteo-a2251-default-rtdb.europe-west1.firebasedatabase.app/"

cred = credentials.Certificate(CRED_FILE)
firebase_admin.initialize_app(cred, {"databaseURL": DB_URL})

CCAA_CODES = ["and","arn","ast","bal","coo","can","cle","clm","cat","val","ext","gal","mad","mur","nav","pva","rio"]

hoy = datetime.now(timezone.utc)
print(f"Fecha actual UTC: {hoy.strftime('%Y-%m-%d')}\n")
print(f"{'CCAA':<6} {'Estado':<10} {'Fecha en texto':<25} {'Lag'}")
print("-" * 60)

patron_fecha = re.compile(
    r"D[ÍI]A\s+(\d+)\s+DE\s+(\w+)\s+DE\s+(\d{4})",
    re.IGNORECASE
)
MESES = {
    "enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,
    "julio":7,"agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12
}

for ccaa in CCAA_CODES:
    ruta = f"/prediccionTexto/ccaa/{ccaa}/hoy"
    datos = db.reference(ruta).get()

    if datos is None:
        print(f"{ccaa:<6} {'AUSENTE':<10} {'—':<25}")
        continue

    texto = str(datos)[:600]
    m = patron_fecha.search(texto)
    if m:
        dia, mes_str, anio = int(m.group(1)), m.group(2).lower(), int(m.group(3))
        mes = MESES.get(mes_str)
        if mes:
            try:
                fecha_texto = datetime(anio, mes, dia, tzinfo=timezone.utc)
                lag = (hoy.date() - fecha_texto.date()).days
                estado = "HOY" if lag == 0 else f"{lag}d VIEJO"
                print(f"{ccaa:<6} {estado:<10} {dia:02d}/{mes:02d}/{anio}  {texto[:35].strip()!r}")
            except ValueError:
                print(f"{ccaa:<6} {'FECHA ERR':<10}")
        else:
            print(f"{ccaa:<6} {'MES DESC':<10} {m.group()}")
    else:
        print(f"{ccaa:<6} {'SIN FECHA':<10} {texto[:60].strip()!r}")
