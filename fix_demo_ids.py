import json, uuid

nb = json.load(open("demo/demo_functions.ipynb", encoding="utf-8"))
fixed = 0
for c in nb["cells"]:
    if "id" not in c or not c.get("id"):
        c["id"] = uuid.uuid4().hex[:8]
        fixed += 1

# Fix avisos area code: replace '72' (Navarra, may lack data) with '61' (Andalucia)
for c in nb["cells"]:
    if c["cell_type"] == "code":
        src = "".join(c["source"])
        if "avisos_cap_ultimo_area" in src and '"72"' in src:
            c["source"] = [line.replace('"72"', '"61"') for line in c["source"]]
            print("Fixed avisos area 72 -> 61")

json.dump(nb, open("demo/demo_functions.ipynb", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"Added {fixed} missing cell IDs, saved")
