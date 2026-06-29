import json

with open("03_prediccion.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

# Cell 3: nacional_hoy, nacional_manana, nacional_pasadomanana
cells[3]["source"] = (
    "from aemetdata.prediccion import nacional_hoy, nacional_manana, nacional_pasadomanana\n"
    "from aemetdata.utils.suport_functions import AemetError\n"
    "\n"
    "try:\n"
    "    pred_hoy = await nacional_hoy([API_KEY])\n"
    '    print(f"Prediccion nacional hoy: {len(pred_hoy)} registros")\n'
    "    display(pd.DataFrame(pred_hoy))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
    "    pred_hoy = []\n"
    "\n"
    "try:\n"
    "    pred_manana = await nacional_manana([API_KEY])\n"
    '    print(f"Prediccion nacional manana: {len(pred_manana)} registros")\n'
    "    display(pd.DataFrame(pred_manana))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
    "    pred_manana = []\n"
    "\n"
    "try:\n"
    "    pred_pasado = await nacional_pasadomanana([API_KEY])\n"
    '    print(f"Prediccion nacional pasado manana: {len(pred_pasado)} registros")\n'
    "    display(pd.DataFrame(pred_pasado))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 4: nacional_manana (now combined into cell 3, skip this or reuse)
cells[4]["source"] = (
    "# pred_manana ya obtenida en la celda anterior\n"
    "if pred_manana:\n"
    '    print(f"Prediccion nacional manana: {len(pred_manana)} registros")\n'
    "    pd.DataFrame(pred_manana)\n"
    "else:\n"
    '    print("Sin datos de prediccion nacional manana")\n'
)

# Cell 5: nacional_medioplazo, nacional_tendencia
cells[5]["source"] = (
    "from aemetdata.prediccion import nacional_medioplazo, nacional_tendencia\n"
    "\n"
    "try:\n"
    "    pred_mplazo = await nacional_medioplazo([API_KEY])\n"
    '    print(f"Prediccion medio plazo: {len(pred_mplazo)} registros")\n'
    "    display(pd.DataFrame(pred_mplazo))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 7: ccaa_hoy
cells[7]["source"] = (
    "from aemetdata.prediccion import ccaa_hoy, ccaa_manana, ccaa_medioplazo\n"
    "\n"
    "try:\n"
    '    pred_ccaa = await ccaa_hoy("83", [API_KEY])  # Madrid\n'
    '    print(f"Prediccion CCAA Madrid hoy: {len(pred_ccaa)} registros")\n'
    "    display(pd.DataFrame(pred_ccaa))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
    "    pred_ccaa = []\n"
)

# Cell 8: ccaa_medioplazo
cells[8]["source"] = (
    "try:\n"
    '    pred_ccaa_mplazo = await ccaa_medioplazo("83", [API_KEY])\n'
    '    print(f"Prediccion CCAA Madrid medio plazo: {len(pred_ccaa_mplazo)} registros")\n'
    "    display(pd.DataFrame(pred_ccaa_mplazo))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 10: provincia_hoy
cells[10]["source"] = (
    "from aemetdata.prediccion import provincia_hoy, provincia_manana\n"
    "\n"
    "try:\n"
    '    pred_prov = await provincia_hoy("28", [API_KEY])\n'
    '    print(f"Prediccion provincia Madrid hoy: {len(pred_prov)} registros")\n'
    "    display(pd.DataFrame(pred_prov))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

with open("03_prediccion.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Fixed cells 3,4,5,7,8,10 in 03_prediccion.ipynb")
