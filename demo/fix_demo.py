import json

with open("demo_functions.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

AE = "from aemetdata.utils.suport_functions import AemetError\n"


def wrap(code: str, extra_import: str = "") -> str:
    """Wrap code in try/except AemetError."""
    indented = "\n".join("    " + line for line in code.strip().split("\n"))
    return (
        (extra_import + "\n" if extra_import else "")
        + "try:\n"
        + indented
        + "\nexcept (AemetError, Exception) as e:\n"
        + '    print(f"Endpoint no disponible: {e}")\n'
    )


# Cell 4: avisos_cap_ultimo_area - wrap
cells[4]["source"] = wrap(
    'from aemetdata.avisos import avisos_cap_ultimo_area\n\narchivos = await avisos_cap_ultimo_area("61", [API_KEY])\nprint(f"Archivos CAP descargados: {list(archivos.keys())[:3]}")',
    AE,
)

# Cell 5: avisos_cap_archivo - wrap
cells[5]["source"] = wrap(
    'from aemetdata.avisos import avisos_cap_archivo\n\narchivos_hist = await avisos_cap_archivo("2026-05-13", "2026-05-15", [API_KEY])\nprint(f"Archivos en el rango: {len(archivos_hist)}")',
    AE,
)

# Cell 8: datos_mensuales - fix 3427Y → 3129, wrap
cells[8]["source"] = wrap(
    'from aemetdata.climatologia import datos_mensuales\nresultado = await datos_mensuales(["3195","3129"], 2020, 2024, [API_KEY])\nprint(f"Tipo: {type(resultado)}")\ndisplay(pd.DataFrame(resultado))',
    AE,
)

# Cell 10: datos_diarios - fix 3427Y → 3129, wrap
cells[10]["source"] = wrap(
    "from aemetdata.climatologia import datos_diarios\nresultado = await datos_diarios([\"3195\",\"3129\"], '2022-01-01', '2022-08-10', [API_KEY])\nprint(f'Tipo: {type(resultado)}')\ndisplay(pd.DataFrame(resultado))",
    AE,
)

# Cell 12: datos_normales - fix 3427Y → 3129, wrap
cells[12]["source"] = wrap(
    'from aemetdata.climatologia import datos_normales\nresultado_normales = await datos_normales(["3195","3129"], [API_KEY])\nprint(f"Tipo: {type(resultado_normales)}")\nimport pandas as pd\ndisplay(pd.DataFrame(resultado_normales))',
    AE,
)

# Cell 14: datos_extremos - fix 3427Y → 3129, wrap
cells[14]["source"] = wrap(
    'from aemetdata.climatologia import datos_extremos\nresultado_extremos_T = await datos_extremos(["3195","3129"], [API_KEY], parametro="T")\nprint(f"Tipo: {type(resultado_extremos_T)}")\ndisplay(pd.DataFrame(resultado_extremos_T))',
    AE,
)

# Cell 16: todas las obs - wrap
cells[16]["source"] = wrap(
    'from aemetdata.observaciones import todas, datos_estacion\n\nobs_todas = await todas([API_KEY])\nprint(f"Estaciones con datos: {len(obs_todas)}")\ndisplay(pd.DataFrame(obs_todas).head(10))',
    AE,
)

# Cell 17: datos_estacion - fix 8416Y → 3129, wrap
cells[17]["source"] = wrap(
    '# Observacion de Madrid Retiro (3195) y Salamanca (3129)\nobs = await datos_estacion(["3195", "3129"], [API_KEY])\nprint(f"Registros: {len(obs)}")\ndisplay(pd.DataFrame(obs))',
    AE,
)

# Cell 19: municipio_diaria - wrap
cells[19]["source"] = wrap(
    'from aemetdata.prediccion import municipio_diaria, municipio_horaria\n\n# 28079 = Madrid, 08019 = Barcelona, 41091 = Sevilla\npred_diaria = await municipio_diaria("28079", [API_KEY])\nprint(f"Prediccion diaria Madrid: {len(pred_diaria)} registros")\ndisplay(pd.DataFrame(pred_diaria))',
    AE,
)

# Cell 20: municipio_horaria - wrap
cells[20]["source"] = wrap(
    'pred_horaria = await municipio_horaria("28079", [API_KEY])\nprint(f"Prediccion horaria Madrid: {len(pred_horaria)} registros")\ndisplay(pd.DataFrame(pred_horaria))',
)

# Cell 21: nacional_hoy - wrap
cells[21]["source"] = wrap(
    'from aemetdata.prediccion import nacional_hoy\n\npred_nac = await nacional_hoy([API_KEY])\nprint(f"Prediccion nacional hoy: {len(pred_nac)} registros")\ndisplay(pd.DataFrame(pred_nac))',
    AE,
)

# Cell 23: todos_municipios - wrap
cells[23]["source"] = wrap(
    'from aemetdata.maestro import todos_municipios, municipio_por_nombre\n\nmunicipios = await todos_municipios([API_KEY])\nprint(f"Total municipios: {len(municipios)}")\ndisplay(pd.DataFrame(municipios).head(10))',
    AE,
)

# Cell 24: municipio_por_nombre - wrap
cells[24]["source"] = wrap(
    "busqueda = await municipio_por_nombre(\"Madrid\", [API_KEY])\nprint(f\"Municipios con 'Madrid': {len(busqueda)}\")\ndisplay(pd.DataFrame(busqueda))",
)

# Cell 26: radar_nacional - wrap
cells[26]["source"] = wrap(
    'from aemetdata.redes import radar_nacional\nfrom IPython.display import Image, display\n\nimg_radar = await radar_nacional([API_KEY])\nprint(f"Radar nacional: {len(img_radar)} bytes")\nif img_radar:\n    display(Image(data=img_radar))',
    AE,
)

# Cell 27: satelite_ndvi - wrap
cells[27]["source"] = wrap(
    'from aemetdata.imagenes import satelite_ndvi\n\nimg_ndvi = await satelite_ndvi([API_KEY])\nprint(f"NDVI satelite: {len(img_ndvi)} bytes")\nif img_ndvi:\n    display(Image(data=img_ndvi))',
    AE,
)

# Cell 30: incendios - wrap
cells[30]["source"] = wrap(
    "from aemetdata.incendios import mapa_riesgo_estimado, mapa_riesgo_previsto\n\nresp_est = await mapa_riesgo_estimado(\"p\", [API_KEY])\nprint(\"Riesgo estimado Peninsula:\", resp_est)\n\nresp_prev = await mapa_riesgo_previsto(\"1\", \"p\", [API_KEY])\nprint(\"Riesgo previsto manana Peninsula:\", resp_prev)",
    AE,
)

with open("demo_functions.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Fixed demo_functions.ipynb")
