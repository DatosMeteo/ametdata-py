import json, os

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjcGFjaGVjby5wZXJlbGxvQGdtYWlsLmNvbSIsImp0aSI6IjE2ZGQxZjJlLTJkMWYtNGI3NS1hYjQ0LWEzNTNhNmQyMjU0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzY4MzgzMjcwLCJ1c2VySWQiOiIxNmRkMWYyZS0yZDFmLTRiNzUtYWI0NC1hMzUzYTZkMjI1NDYiLCJyb2xlIjoiIn0.4eP7KwIbUfdq91ZrcPYEwPhUgPN1sUhCyIZdrieHnc0"

NOTEBOOK_META = {
    "kernelspec": {
        "display_name": "Python 3.11 (aemetdata)",
        "language": "python",
        "name": "python311"
    },
    "language_info": {
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "version": "3.11.6"
    }
}

def code_cell(src):
    return {"cell_type": "code", "execution_count": None,
            "metadata": {}, "outputs": [], "source": src}

def md_cell(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}

def setup_lines(extra_import=None):
    lines = [
        "# Instala el paquete (solo la primera vez)\n",
        "!pip install -q aemetdata nest_asyncio\n",
        "\n",
        "# -- API Key ---------------------------------------------------------\n",
        f'API_KEY = "{API_KEY}"\n',
        "\n",
        "# En Google Colab guarda tu clave como secreto con nombre AEMET_API_KEY\n",
        "try:\n",
        "    from google.colab import userdata\n",
        '    API_KEY = userdata.get("AEMET_API_KEY") or API_KEY\n',
        "except Exception:\n",
        "    pass\n",
        "\n",
        "import nest_asyncio; nest_asyncio.apply()\n",
        "import pandas as pd\n",
    ]
    if extra_import:
        lines.append(extra_import + "\n")
    lines.append('print(f"Listo. API key: {API_KEY[:8]}...")\n')
    return lines


# ---------------------------------------------------------------------------
# 1. Patch setup cell in all notebooks
# ---------------------------------------------------------------------------
NBS = sorted(f for f in os.listdir(".") if f.endswith(".ipynb"))

for nb in NBS:
    data = json.load(open(nb, encoding="utf-8"))
    code_idxs = [i for i, c in enumerate(data["cells"]) if c["cell_type"] == "code"]
    if not code_idxs:
        continue

    needs_display = nb in ("05_redes_e_imagenes.ipynb",)
    extra = "from IPython.display import Image, display" if needs_display else None

    data["cells"][code_idxs[0]]["source"] = setup_lines(extra)
    data["metadata"] = NOTEBOOK_META

    with open(nb, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    print(f"Patched setup: {nb} ({len(data['cells'])} cells)")


# ---------------------------------------------------------------------------
# 2. Complete demo_functions.ipynb with missing sections
# ---------------------------------------------------------------------------
DEMO = "demo_functions.ipynb"
data = json.load(open(DEMO, encoding="utf-8"))

# Keep only up to and including the existing climatologia section (first 15 cells)
# Then append the missing sections
extra_cells = [

    # ---- Observaciones ----
    md_cell(["## 4. Observaciones\n",
             "\n",
             "Observaciones en tiempo real de todas las estaciones (últimas 24 h).\n"]),

    code_cell([
        "from aemetdata.observaciones import todas, datos_estacion\n",
        "\n",
        "obs_todas = await todas([API_KEY])\n",
        'print(f"Estaciones con datos: {len(obs_todas)}")\n',
        "pd.DataFrame(obs_todas).head(10)\n",
    ]),

    code_cell([
        '# Observacion de Madrid Retiro (3195) y Malaga aeropuerto (8416Y)\n',
        'obs = await datos_estacion(["3195", "8416Y"], [API_KEY])\n',
        'print(f"Registros: {len(obs)}")\n',
        'pd.DataFrame(obs)\n',
    ]),

    # ---- Prediccion ----
    md_cell(["## 5. Predicción\n",
             "\n",
             "Predicciones por municipio (diaria y horaria) y predicción nacional.\n"]),

    code_cell([
        "from aemetdata.prediccion import municipio_diaria, municipio_horaria\n",
        "\n",
        '# 28079 = Madrid, 08019 = Barcelona, 41091 = Sevilla\n',
        'pred_diaria = await municipio_diaria("28079", [API_KEY])\n',
        'print(f"Prediccion diaria Madrid: {len(pred_diaria)} registros")\n',
        'pd.DataFrame(pred_diaria)\n',
    ]),

    code_cell([
        'pred_horaria = await municipio_horaria("28079", [API_KEY])\n',
        'print(f"Prediccion horaria Madrid: {len(pred_horaria)} registros")\n',
        'pd.DataFrame(pred_horaria)\n',
    ]),

    code_cell([
        "from aemetdata.prediccion import nacional_hoy\n",
        "\n",
        "pred_nac = await nacional_hoy([API_KEY])\n",
        'print(f"Prediccion nacional hoy: {len(pred_nac)} registros")\n',
        "pd.DataFrame(pred_nac)\n",
    ]),

    # ---- Maestro ----
    md_cell(["## 6. Maestro de municipios\n",
             "\n",
             "Catálogo completo de municipios de España. "
             "Útil para obtener los códigos que necesitan las predicciones.\n"]),

    code_cell([
        "from aemetdata.maestro import todos_municipios, municipio_por_nombre\n",
        "\n",
        "municipios = await todos_municipios([API_KEY])\n",
        'print(f"Total municipios: {len(municipios)}")\n',
        "pd.DataFrame(municipios).head(10)\n",
    ]),

    code_cell([
        'busqueda = await municipio_por_nombre("Madrid", [API_KEY])\n',
        'print(f"Municipios con \'Madrid\': {len(busqueda)}")\n',
        "pd.DataFrame(busqueda)\n",
    ]),

    # ---- Radar / Imagenes ----
    md_cell(["## 7. Radar e imágenes de satélite\n"]),

    code_cell([
        "from aemetdata.redes import radar_nacional\n",
        "from IPython.display import Image, display\n",
        "\n",
        "img_radar = await radar_nacional([API_KEY])\n",
        'print(f"Radar nacional: {len(img_radar)} bytes")\n',
        "if img_radar:\n",
        "    display(Image(data=img_radar))\n",
    ]),

    code_cell([
        "from aemetdata.imagenes import satelite_ndvi\n",
        "\n",
        "img_ndvi = await satelite_ndvi([API_KEY])\n",
        'print(f"NDVI satelite: {len(img_ndvi)} bytes")\n',
        "if img_ndvi:\n",
        "    display(Image(data=img_ndvi))\n",
    ]),

    # ---- Avisos ----
    md_cell(["## 8. Avisos meteorológicos (CAP)\n"]),

    code_cell([
        "from aemetdata.avisos import avisos_cap_ultimo_area\n",
        "\n",
        '# 61=Andalucia, 77=Madrid, 69=Cataluna\n',
        'archivos = await avisos_cap_ultimo_area("61", [API_KEY])\n',
        'print(f"Archivos CAP area 61 (Andalucia): {len(archivos)}")\n',
        "for k in list(archivos.keys())[:3]:\n",
        '    print(f"  {k}")\n',
    ]),

    # ---- Incendios ----
    md_cell(["## 9. Riesgo de incendios forestales\n"]),

    code_cell([
        "from aemetdata.incendios import mapa_riesgo_estimado, mapa_riesgo_previsto\n",
        "\n",
        "# area: 'p'=Peninsula, 'b'=Baleares, 'c'=Canarias\n",
        'resp_est = await mapa_riesgo_estimado("p", [API_KEY])\n',
        'print("Riesgo estimado Peninsula:", resp_est)\n',
        "\n",
        '# dia: 1=manana, 2=pasado manana, 3=en 3 dias\n',
        'resp_prev = await mapa_riesgo_previsto("1", "p", [API_KEY])\n',
        'print("Riesgo previsto manana:", resp_prev)\n',
    ]),
]

# Check which sections already exist to avoid duplicates
existing = "\n".join("".join(c.get("source", [])) for c in data["cells"])

cells_to_add = []
for cell in extra_cells:
    src = "".join(cell.get("source", []))
    # Check by unique function name or section header
    marker = src.strip().split("\n")[0][:60]
    if marker not in existing:
        cells_to_add.append(cell)

data["cells"].extend(cells_to_add)
data["metadata"] = NOTEBOOK_META

with open(DEMO, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)

print(f"\nCompleted {DEMO}: now {len(data['cells'])} cells (+{len(cells_to_add)} new)")

# ---------------------------------------------------------------------------
# 3. Final verification
# ---------------------------------------------------------------------------
print("\n=== Final verification ===")
for nb in NBS:
    data = json.load(open(nb, encoding="utf-8"))
    code_cells = [c for c in data["cells"] if c["cell_type"] == "code"]
    src0 = "".join(code_cells[0]["source"]) if code_cells else ""
    ks = data.get("metadata", {}).get("kernelspec", {}).get("name", "NONE")
    ok = all([
        "nest_asyncio" in src0,
        "!pip install" in src0,
        "eyJhbGciOiJIUzI1NiJ9" in src0,
        ks == "python311",
    ])
    print(f"{'OK  ' if ok else 'FAIL'} {nb} ({len(data['cells'])} cells, kernel={ks})")
    if not ok:
        if "nest_asyncio" not in src0: print("     missing: nest_asyncio")
        if "!pip install" not in src0:  print("     missing: pip install")
        if ks != "python311":            print(f"     bad kernel: {ks}")
