import os, re, firebase_admin
from firebase_admin import credentials, db

BASE = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(BASE,'..','Firebase-Acces','datosmeteo-a2251-firebase-adminsdk-fbsvc-2f03734ac0.json'))
firebase_admin.initialize_app(cred, {'databaseURL': 'https://datosmeteo-a2251-default-rtdb.europe-west1.firebasedatabase.app/'})

for plazo in ['hoy','manana','medioplazo','tendencia']:
    datos = db.reference('/prediccionTexto/nacional/' + plazo).get()
    if datos:
        m = re.search(r'DIA\s+\d+\s+DE\s+\w+\s+DE\s+\d{4}', str(datos)[:300], re.I)
        print("nacional/" + plazo + ": TIENE | " + (m.group() if m else "sin fecha") + " | len=" + str(len(str(datos))))
    else:
        print("nacional/" + plazo + ": AUSENTE")
