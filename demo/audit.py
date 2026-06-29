import json, os, sys

# Fix demo_functions.ipynb setup cell
CORRECT_SETUP = [
    "# Instala el paquete (solo la primera vez)\n",
    "!pip install -q aemetdata\n",
    "\n",
    "# \u2500\u2500 API Key \u2500\u2500\u2500 Pon aqu\u00ed tu clave de https://opendata.aemet.es \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n",
    "API_KEY = \"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjcGFjaGVjby5wZXJlbGxvQGdtYWlsLmNvbSIsImp0aSI6IjE2ZGQxZjJlLTJkMWYtNGI3NS1hYjQ0LWEzNTNhNmQyMjU0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzY4MzgzMjcwLCJ1c2VySWQiOiIxNmRkMWYyZS0yZDFmLTRiNzUtYWI0NC1hMzUzYTZkMjI1NDYiLCJyb2xlIjoiIn0.4eP7KwIbUfdq91ZrcPYEwPhUgPN1sUhCyIZdrieHnc0\"\n",
    "\n",
    "# En Google Colab puedes guardarla como secreto (icono llave en el panel lateral)\n",
    "try:\n",
    "    from google.colab import userdata\n",
    "    API_KEY = userdata.get(\"AEMET_API_KEY\") or API_KEY\n",
    "except Exception:\n",
    "    pass\n",
    "\n",
    "import pandas as pd\n",
    "print(f\"Listo. API key: {API_KEY[:8]}...\")\n"
]

path = 'demo_functions.ipynb'
data = json.load(open(path, encoding='utf-8'))

# Find and fix the broken setup cell (first code cell with !pip install)
for i, cell in enumerate(data['cells']):
    if cell['cell_type'] == 'code' and any('!pip install' in s for s in cell['source']):
        data['cells'][i]['source'] = CORRECT_SETUP
        print(f'Fixed setup cell (index {i})')
        break

# Remove redundant "import pandas as pd" cell right after setup if present
cells = data['cells']
for i in range(len(cells) - 1, -1, -1):
    cell = cells[i]
    if cell['cell_type'] == 'code' and ''.join(cell['source']).strip() == 'import pandas as pd':
        # Only remove if the previous cell is the setup cell we just fixed
        if i > 0 and any('!pip install' in s for s in cells[i-1]['source']):
            cells.pop(i)
            print(f'Removed redundant pandas import cell (was index {i})')
            break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
print('Done.')

for nb in nbs:
    data = json.load(open(nb, encoding='utf-8'))
    print('=== ' + nb + ' ===')
    for i, cell in enumerate(data['cells'], 1):
        src = ''.join(cell['source'])
        ct = cell['cell_type']
        preview = src.replace('\n', ' | ')[:200]
        print('  C' + str(i) + ' (' + ct + '): ' + preview)
    print()

BAD_META = (
    '"metadata": { "kernelspec": {"display_name": "Python 3.11 (aemetdata)", '
    '"language": "python", "name": "python311"}, "language_info": '
    '{"codemirror_mode": {"name": "ipython", "version": 3}, "file_extension": ".py", '
    '"mimetype": "text/x-python", "name": "python", "pygments_lexer": "ipython3", '
    '"version": "3.11.6"},}'
)

GOOD_NOTEBOOK_META = {
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

for nb in broken:
    txt = open(nb, encoding='utf-8').read()
    # Fix bad cell metadata
    txt = txt.replace(BAD_META, '"metadata": {}')
    # Parse what we have
    try:
        data = json.loads(txt)
    except Exception as e:
        print('STILL BROKEN: ' + nb + ' -> ' + str(e))
        continue
    # Set correct notebook-level metadata
    data['metadata'] = GOOD_NOTEBOOK_META
    with open(nb, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    print('Fixed: ' + nb)

# Verify all
print()
for nb in sorted(f for f in os.listdir('.') if f.endswith('.ipynb')):
    try:
        data = json.load(open(nb, encoding='utf-8'))
        ks = data.get('metadata', {}).get('kernelspec', {}).get('name', 'NONE')
        print('OK  ' + nb + ' (' + str(len(data['cells'])) + ' cells, kernel=' + ks + ')')
    except Exception as e:
        print('ERR ' + nb + ' -> ' + str(e)[:80])

