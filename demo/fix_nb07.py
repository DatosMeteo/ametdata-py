import json

with open("07_antartida_y_maestro.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

# Cell 3: datos_antartida
cells[3]["source"] = (
    "from aemetdata.antartida import datos_antartida\n"
    "from aemetdata.utils.suport_functions import AemetError\n"
    "\n"
    "try:\n"
    "    datos = await datos_antartida(\n"
    '        fecha_inicio="2024-01-01T00:00:00UTC",\n'
    '        fecha_fin="2024-01-31T23:59:59UTC",\n'
    '        identificacion="89064",\n'
    "        api_keys=[API_KEY],\n"
    "    )\n"
    '    print(f"Registros obtenidos (BAE Juan Carlos I): {len(datos)}")\n'
    "    display(pd.DataFrame(datos))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
    "    datos = []\n"
)

# Cell 4: datos_antartida (ambas estaciones)
cells[4]["source"] = (
    "try:\n"
    "    datos_dos = await datos_antartida(\n"
    '        fecha_inicio="2024-01-01T00:00:00UTC",\n'
    '        fecha_fin="2024-01-31T23:59:59UTC",\n'
    '        identificacion=["89064", "89070"],\n'
    "        api_keys=[API_KEY],\n"
    "    )\n"
    '    print(f"Registros combinados (ambas estaciones): {len(datos_dos)}")\n'
    "    display(pd.DataFrame(datos_dos))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 6: todos_municipios
cells[6]["source"] = (
    "from aemetdata.maestro import todos_municipios\n"
    "\n"
    "try:\n"
    "    municipios = await todos_municipios([API_KEY])\n"
    '    print(f"Total de municipios en el catalogo: {len(municipios)}")\n'
    "    df_mun = pd.DataFrame(municipios)\n"
    "    display(df_mun.head(10))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
    "    municipios = []\n"
    "    df_mun = pd.DataFrame()\n"
)

# Cell 7: columnas disponibles
cells[7]["source"] = (
    "if not df_mun.empty:\n"
    '    print("Columnas:", df_mun.columns.tolist())\n'
    "else:\n"
    '    print("Sin datos")\n'
)

# Cell 8: municipio por id
cells[8]["source"] = (
    "from aemetdata.maestro import municipio\n"
    "\n"
    "try:\n"
    '    datos_madrid = await municipio("id28079", [API_KEY])\n'
    '    print("Datos del municipio id28079 (Madrid):")\n'
    "    display(pd.DataFrame(datos_madrid))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 9: municipio_por_nombre Sevilla
cells[9]["source"] = (
    "from aemetdata.maestro import municipio_por_nombre\n"
    "\n"
    "try:\n"
    '    resultados = await municipio_por_nombre("Sevilla", [API_KEY])\n'
    '    print(f"Municipios encontrados con \'Sevilla\': {len(resultados)}")\n'
    "    display(pd.DataFrame(resultados))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 10: municipio_por_nombre Barcelona
cells[10]["source"] = (
    "try:\n"
    '    barna = await municipio_por_nombre("Barcelona", [API_KEY])\n'
    "    df_barna = pd.DataFrame(barna)\n"
    "    print(\"Resultados para 'Barcelona':\")\n"
    "    print(df_barna.to_string())\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

with open("07_antartida_y_maestro.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Fixed cells in 07_antartida_y_maestro.ipynb")
