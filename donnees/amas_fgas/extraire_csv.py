"""Extrait (nom, z, fgas, sigma_fgas) de la Table 2 de Mantz et al. 2014
(arxiv_src/fgas_table.tex, source arXiv:1402.6212) vers un CSV.
f_gas mesure dans la coquille spherique 0.8-1.2 r2500 (cosmologie de reference du papier)."""
import re
import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "arxiv_src", "fgas_table.tex")
OUT = os.path.join(BASE, "mantz2014_fgas_r2500shell.csv")

rows = []
with open(SRC, encoding="utf-8") as f:
    for line in f:
        if "&" not in line or "pm" not in line:
            continue
        cells = line.split("&")
        name = cells[0].strip()
        if name.startswith("\\") or "Cluster" in name or not name:
            continue
        name = name.replace("~", " ").replace("$-$", "-").strip()
        z = float(cells[1].strip())
        # la derniere paire $a\pm b$ de la ligne est fgas (l'avant-derniere est M2500)
        pms = re.findall(r"\$([\d.]+)\\pm([\d.]+)\$", line)
        fgas, sig = pms[-1]
        rows.append((name, z, float(fgas), float(sig)))

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["nom", "z", "fgas", "sigma_fgas"])
    for r in rows:
        w.writerow(r)

print("lignes:", len(rows))
zs = [r[1] for r in rows]
print("z min/max:", min(zs), max(zs))
print("premier:", rows[0], " dernier:", rows[-1])
