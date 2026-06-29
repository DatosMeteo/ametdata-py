import json

with open("02_climatologia.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

# Fix cell 21 - rejillas_anuales: use correct area 'pnb' and wrap in try/except
cells[21]["source"] = (
    "from aemetdata.climatologia import rejillas_anuales, rejillas_mensuales\n"
    "from aemetdata.utils.suport_functions import AemetError\n"
    "\n"
    "# area: 'pnb' (Peninsula+Baleares), 'can' (Canarias)\n"
    "# Nota: estos endpoints devuelven GeoTIFF binario, no JSON.\n"
    "try:\n"
    '    rejilla_anual = await rejillas_anuales("pnb", "ta", "2023", [API_KEY])\n'
    '    print(f"Datos rejilla anual 2023: {len(rejilla_anual)} registros")\n'
    "    print(pd.DataFrame(rejilla_anual).head(5))\n"
    "except AemetError as e:\n"
    '    print(f"Este endpoint devuelve GeoTIFF binario (no JSON): {e}")\n'
)

# Fix cell 22 - rejillas_mensuales: use correct area 'pnb' and wrap in try/except
cells[22]["source"] = (
    "try:\n"
    '    rejilla_mensual = await rejillas_mensuales("pnb", "prec", "2024", "01", [API_KEY])\n'
    '    print(f"Datos rejilla mensual enero 2024: {len(rejilla_mensual)} registros")\n'
    "    print(pd.DataFrame(rejilla_mensual).head(5))\n"
    "except AemetError as e:\n"
    '    print(f"Este endpoint devuelve GeoTIFF binario (no JSON): {e}")\n'
)

with open("02_climatologia.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Fixed cells 21 and 22 in 02_climatologia.ipynb")
