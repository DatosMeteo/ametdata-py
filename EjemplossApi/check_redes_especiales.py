"""Inspecciona la estructura guardada en Firebase para ozono y radiación"""
import os, json, firebase_admin
from firebase_admin import credentials, db

BASE = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(BASE,'..','Firebase-Acces','datosmeteo-a2251-firebase-adminsdk-fbsvc-2f03734ac0.json'))
firebase_admin.initialize_app(cred, {'databaseURL': 'https://datosmeteo-a2251-default-rtdb.europe-west1.firebasedatabase.app/'})

print("=== OZONO ===")
ozono = db.reference('/redEspecial/ozono').get()
if ozono:
    print("tipo:", type(ozono).__name__)
    print("keys:", list(ozono.keys()) if isinstance(ozono, dict) else "N/A")
    print(json.dumps(ozono, ensure_ascii=False, indent=2)[:1500])
else:
    print("AUSENTE")

print("\n=== RADIACION (primeras 500 chars) ===")
rad = db.reference('/redEspecial/radiacion').get()
if rad:
    print("tipo:", type(rad).__name__)
    if isinstance(rad, dict):
        print("keys:", list(rad.keys()))
        print("headers:", rad.get('headers', [])[:10])
        print("num filas:", len(rad.get('filas', [])))
        if rad.get('filas'):
            print("primera fila (primeros 10 cols):", rad['filas'][0][:10])
    print(str(rad)[:500])
else:
    print("AUSENTE")
