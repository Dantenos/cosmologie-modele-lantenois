#!/usr/bin/env python3
"""genere_audience v1 — le visuel du Rôle (prédictions futures et leur suivi), 24/08/2026.
CRITERES PRE-ENREGISTRES (geles) : le HTML n'est ECRIT que si (1) outils/audience.json
contient exactement les 4 affaires connues avec leurs hash d'inscription du 22/08/2026
(DR3-beta dc8ab8e53b9f ; FRB-s d103d6ebbcf0 ; W-universel b652a956509b ; k3-vs-0
fbf93c9a69b6) — un hash different signifierait une affaire reecrite apres inscription ;
(2) sha256(outils/scelle.py) est exactement le hash publie 68d06bcc... ; (3) la table FRB
de Connor 2025 compte exactement 69 lignes (le compteur affiche est recompte, pas recopie).
Sinon : REFUS, rien n'est emis. Les jauges du gabarit citent leurs entrees de registre
(#139, #141-151) ; toute mise a jour des chiffres passe par le gabarit ET par perime.py.
Usage : python3 outils/genere_audience.py  ->  visuels/le_role.html
"""
import sys, json, csv, hashlib, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
HASHES = {"DR3-beta": "dc8ab8e53b9f", "FRB-s": "d103d6ebbcf0",
          "W-universel": "b652a956509b", "k3-vs-0": "fbf93c9a69b6"}
SCEAU = "68d06bcccbecf2276919c05dc841c6d878ca2516427e533af38d64344aed45a2"

def main():
    aud = json.loads((ROOT / "outils/audience.json").read_text(encoding="utf-8"))
    aff = aud["affaires"]
    if set(aff) != set(HASHES) or any(aff[k]["hash"] != v for k, v in HASHES.items()):
        sys.exit("[role] REFUS : les affaires ou leurs hash d'inscription ne correspondent pas au 22/08/2026")
    if hashlib.sha256((ROOT / "outils/scelle.py").read_bytes()).hexdigest() != SCEAU:
        sys.exit("[role] REFUS : le sceau a change — aucun visuel n'est emis sur un arbitre altere")
    n_frb = len(list(csv.DictReader((ROOT / "donnees/frb_connor2025/frbsample_connor0924.csv").open(encoding="utf-8"))))
    if n_frb != 69:
        sys.exit(f"[role] REFUS : {n_frb} FRB dans la table (gabarit calibre pour 69 — mettre a jour compteur ET gabarit)")
    tpl = (ROOT / "outils/audience_template.html").read_text(encoding="utf-8")
    ten = json.loads((ROOT / "outils/tensions.json").read_text(encoding="utf-8"))["tensions"]
    ten_min = [dict(id=t["id"], statut=t["statut"], enonce=t["enonce"], magnitude=t["magnitude"],
                    lectures=t["lectures"], arbitre=t["arbitre"]) for t in ten]
    out = tpl.replace("__DATE__", str(datetime.date.today())).replace("__TENSIONS__", json.dumps(ten_min, ensure_ascii=False))
    dest = ROOT / "visuels/le_role.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[role] ecrit : {dest.name} ({dest.stat().st_size//1024} ko) — 4 affaires, hash verifies, sceau intact, N(FRB) = {n_frb}")

if __name__ == "__main__":
    main()
