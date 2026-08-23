#!/usr/bin/env python3
"""genere_atlas v1 — le visuel de l'atlas, GÉNÉRÉ depuis atlas_leaderboard.json (24/08/2026).
CRITERES PRE-ENREGISTRES (geles) : le HTML n'est ECRIT que si le leaderboard existe, contient
exactement 19 modeles, et que ses chiffres de tete correspondent au registre (#150 : les deux
iLCDM en tete, accretion chi2 = 1419,309 +/- 0,01). Sinon REFUS — le visuel ne doit jamais
diverger du JSON, qui lui-meme n'est ecrit que par atlas_v1.py (gele) apres validation.
Zero dependance reseau dans la sortie. Usage : python3 outils/genere_atlas.py
"""
import sys, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEAD = ROOT / "registres" / "atlas_leaderboard.json"

def main():
    if not LEAD.exists(): sys.exit("[atlas-visuel] REFUS : leaderboard absent (lancer scripts/atlas_v1.py)")
    d = json.loads(LEAD.read_text(encoding="utf-8"))
    noms = [m["nom"] for m in d["modeles"]]
    acc = next(m for m in d["modeles"] if m["nom"].startswith("ACCRETION (Gamma"))
    if not (len(d["modeles"]) == 19 and noms[0].startswith("iLCDM") and noms[1].startswith("iLCDM")
            and abs(acc["chi2"] - 1419.309) < 0.01):
        sys.exit(f"[atlas-visuel] REFUS : leaderboard inattendu ({len(d['modeles'])} modeles, tete {noms[0]!r}, acc {acc['chi2']})")
    tpl = (ROOT / "outils" / "atlas_template.html").read_text(encoding="utf-8")
    out = tpl.replace("__DATA__", json.dumps(d, ensure_ascii=False)).replace("__DATE__", d["date"])
    dest = ROOT / "visuels" / "atlas.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[atlas-visuel] ecrit : {dest.name} ({dest.stat().st_size//1024} ko) — 19 modeles, tete iLCDM, accretion 1419,309 : conformes #150")

if __name__ == "__main__":
    main()
