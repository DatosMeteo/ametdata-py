import json

with open("03_prediccion.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

# Cell 12: municipio_diaria
cells[12]["source"] = (
    "from aemetdata.prediccion import municipio_diaria\n"
    "from aemetdata.utils.suport_functions import AemetError\n"
    "\n"
    "try:\n"
    '    pred_mun_d = await municipio_diaria("28079", [API_KEY])\n'
    '    print(f"Prediccion diaria Madrid: {len(pred_mun_d)} registros")\n'
    "    display(pd.DataFrame(pred_mun_d))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 13: municipio_horaria
cells[13]["source"] = (
    "from aemetdata.prediccion import municipio_horaria\n"
    "\n"
    "try:\n"
    '    pred_mun_h = await municipio_horaria("28079", [API_KEY])\n'
    '    print(f"Prediccion horaria Madrid: {len(pred_mun_h)} registros")\n'
    "    display(pd.DataFrame(pred_mun_h))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 15: playa
cells[15]["source"] = (
    "from aemetdata.prediccion import playa\n"
    "\n"
    "# 0304201001 = Playa de la Barceloneta (Barcelona)\n"
    "try:\n"
    '    pred_playa = await playa("0304201001", [API_KEY])\n'
    '    print(f"Prediccion playa: {len(pred_playa)} registros")\n'
    "    display(pd.DataFrame(pred_playa))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 17: uvi
cells[17]["source"] = (
    "from aemetdata.prediccion import uvi\n"
    "\n"
    "# dia: '0' = hoy, '1' = manana, '2' = pasado, '3' = en 3 dias\n"
    "try:\n"
    '    pred_uvi = await uvi("0", [API_KEY])\n'
    '    print(f"Prediccion UVI hoy: {len(pred_uvi)} registros")\n'
    "    display(pd.DataFrame(pred_uvi).head(10))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 19: maritima_costera
cells[19]["source"] = (
    "from aemetdata.prediccion import maritima_costera, maritima_altamar\n"
    "\n"
    "# Costas: '101' = Costa Cantabrica occidental, '121' = Costa Mediterranea nordeste...\n"
    "try:\n"
    '    pred_costera = await maritima_costera("101", [API_KEY])\n'
    '    print(f"Prediccion maritima costera 101: {len(pred_costera)} registros")\n'
    "    display(pd.DataFrame(pred_costera))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 20: maritima_altamar
cells[20]["source"] = (
    "# Alta mar\n"
    "try:\n"
    '    pred_altamar = await maritima_altamar("11", [API_KEY])\n'
    '    print(f"Prediccion altamar 11: {len(pred_altamar)} registros")\n'
    "    display(pd.DataFrame(pred_altamar))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 22: nivologica
cells[22]["source"] = (
    "from aemetdata.prediccion import nivologica\n"
    "\n"
    "# Zonas: 'pir' = Pirineos, 'can' = Cordillera Cantabrica, 'sib' = Sistema Iberica\n"
    "try:\n"
    '    pred_nivo = await nivologica("pir", [API_KEY])\n'
    '    print(f"Prediccion nivologica Pirineos: {len(pred_nivo)} registros")\n'
    "    display(pd.DataFrame(pred_nivo))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

with open("03_prediccion.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Fixed remaining cells in 03_prediccion.ipynb")
