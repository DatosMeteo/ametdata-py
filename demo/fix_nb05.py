import json

with open("05_redes_e_imagenes.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

# Cell 3: radar_nacional
cells[3]["source"] = (
    "from aemetdata.redes import radar_nacional\n"
    "from aemetdata.utils.suport_functions import AemetError\n"
    "\n"
    "try:\n"
    "    imagen_radar = await radar_nacional([API_KEY])\n"
    '    print(f"Bytes descargados: {len(imagen_radar)}")\n'
    "    if imagen_radar:\n"
    "        display(Image(data=imagen_radar))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 5: radar_regional CAT
cells[5]["source"] = (
    "from aemetdata.redes import radar_regional\n"
    "\n"
    "try:\n"
    '    imagen_regional = await radar_regional("CAT", [API_KEY])  # Cataluna\n'
    '    print(f"Bytes descargados (radar CAT): {len(imagen_regional)}")\n'
    "    if imagen_regional:\n"
    "        display(Image(data=imagen_regional))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 7: rayos_mapa (already has some logic, just wrap it)
cells[7]["source"] = (
    "from aemetdata.redes import rayos_mapa\n"
    "\n"
    "try:\n"
    "    resp_rayos = await rayos_mapa([API_KEY])\n"
    '    print("Respuesta API rayos:")\n'
    "    print(resp_rayos)\n"
    '    if resp_rayos.get("datos"):\n'
    "        from aemetdata.utils.suport_functions import fetch_bytes_url\n"
    '        img_rayos = await fetch_bytes_url(resp_rayos["datos"])\n'
    "        if img_rayos:\n"
    "            display(Image(data=img_rayos))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 9: contaminacion_fondo
cells[9]["source"] = (
    "from aemetdata.redes import contaminacion_fondo\n"
    "\n"
    "try:\n"
    '    resp_cont = await contaminacion_fondo("CBA", "BEN", [API_KEY])\n'
    '    print("Contaminacion de fondo:")\n'
    "    print(resp_cont)\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 11: ozono
cells[11]["source"] = (
    "from aemetdata.redes import ozono, perfil_ozono\n"
    "\n"
    "try:\n"
    '    resp_ozono = await ozono("EL", [API_KEY])  # El Arenosillo\n'
    '    print("Datos de ozono:")\n'
    "    print(resp_ozono)\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 12: perfil_ozono
cells[12]["source"] = (
    "try:\n"
    '    resp_perfil = await perfil_ozono("EL", [API_KEY])\n'
    '    print("Perfil vertical de ozono:")\n'
    "    print(resp_perfil)\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 14: radiacion
cells[14]["source"] = (
    "from aemetdata.redes import radiacion\n"
    "\n"
    "try:\n"
    '    resp_rad = await radiacion("SEV", "GHI", [API_KEY])  # Sevilla, GHI\n'
    '    print("Radiacion solar (SEV, GHI):")\n'
    "    print(resp_rad)\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 16: satelite_ndvi
cells[16]["source"] = (
    "from aemetdata.imagenes import satelite_ndvi\n"
    "\n"
    "try:\n"
    "    img_ndvi = await satelite_ndvi([API_KEY])\n"
    '    print(f"NDVI descargado: {len(img_ndvi)} bytes")\n'
    "    if img_ndvi:\n"
    "        display(Image(data=img_ndvi))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

# Cell 17: satelite_sst
cells[17]["source"] = (
    "from aemetdata.imagenes import satelite_sst\n"
    "\n"
    "try:\n"
    "    img_sst = await satelite_sst([API_KEY])\n"
    '    print(f"SST descargado: {len(img_sst)} bytes")\n'
    "    if img_sst:\n"
    "        display(Image(data=img_sst))\n"
    "except AemetError as e:\n"
    '    print(f"Endpoint no disponible: {e}")\n'
)

with open("05_redes_e_imagenes.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Fixed cells in 05_redes_e_imagenes.ipynb")
