import json

with open("02_climatologia.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

for i, cell in enumerate(cells):
    src = "".join(cell.get("source", []))
    if "8416Y" in src:
        new_src = src.replace('"8416Y"', '"3196"')
        cells[i]["source"] = new_src
        print(f"Cell {i}: replaced 8416Y with 3196")

with open("02_climatologia.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done.")
