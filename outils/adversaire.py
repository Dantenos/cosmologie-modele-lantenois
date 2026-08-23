#!/usr/bin/env python3
"""adversaire v1 — audit contradictoire automatisé. Né le 24/08/2026 du corpus cosmologie.

RÈGLE CONSTITUTIVE : l'agent n'émet AUCUNE opinion — seulement des attaques exécutables.
Une attaque est un script qui imprime `ADVERSAIRE: <nom_affirmation> <valeur_calculée>`.
Toute affirmation du manifeste sans valeur exécutée = NON REPRODUITE (jamais « douteuse »,
jamais un avis). Une critique inventée ne compile pas : c'est la défense anti-hallucination.

CRITÈRES PRÉ-ENREGISTRÉS DE V1 (gelés par registre.py) :
  - v1 réussit si : l'audit fondateur (Croker et al. 2024, classe « fond cosmologique »)
    produit un rapport où chaque verdict provient d'une valeur exécutée, comparée à la
    valeur publiée sous tolérance déclarée dans le manifeste.
  - v1 échoue si : un verdict apparaît sans valeur exécutée correspondante.
  - Réciprocité : adversaire.py et chaque script d'attaque sont gelés par registre AVANT
    l'exécution de l'audit.

Manifeste (JSON) : {"papier": id, "affirmations": [{"nom", "publie", "tolerance", "unite"}],
                    "attaques": ["script.py", ...]}
Usage : adversaire.py audit manifeste.json
"""
import sys, json, subprocess, pathlib, datetime

def audit(mpath):
    m = json.loads(pathlib.Path(mpath).read_text(encoding="utf-8"))
    # réciprocité : tout doit être gelé avant exécution
    r = subprocess.run([sys.executable, "registre.py", "verify", "adversaire.py", *m["attaques"]],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("[adversaire] REFUS : outil ou attaques non gelés par registre.\n" + r.stdout)
    mesures = {}
    for att in m["attaques"]:
        print(f"[adversaire] exécution : {att}")
        p = subprocess.run([sys.executable, att], capture_output=True, text=True, timeout=3000)
        for ligne in p.stdout.splitlines():
            if ligne.startswith("ADVERSAIRE:"):
                _, nom, val = ligne.split(None, 2)
                mesures[nom] = float(val)
    lignes = [f"# RAPPORT D'AUDIT — {m['papier']}",
              f"*généré le {datetime.date.today()} par adversaire v1 ; outil et attaques gelés par registre*",
              "", "| affirmation | publié | exécuté | tolérance | verdict |", "|---|---|---|---|---|"]
    ok = True
    for a in m["affirmations"]:
        v = mesures.get(a["nom"])
        if v is None:
            verdict, ex = "**NON REPRODUITE**", "—"
        else:
            ecart = abs(v - a["publie"])
            verdict = "VALIDÉE" if ecart <= a["tolerance"] else "**RÉFUTÉE**"
            ex = f"{v:.4g}"
        ok &= verdict != "**NON REPRODUITE**" or False
        lignes.append(f"| {a['nom']} | {a['publie']} {a.get('unite','')} | {ex} | ±{a['tolerance']} | {verdict} |")
    lignes += ["", "Règle appliquée : aucune opinion — chaque verdict provient d'une valeur exécutée.",
               "Rétractations éventuelles : RETRACTATIONS.md (via registre)."]
    out = pathlib.Path(f"RAPPORT_{m['papier']}.md")
    out.write_text("\n".join(lignes), encoding="utf-8")
    print(f"[adversaire] rapport écrit : {out}")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "audit": audit(sys.argv[2])
    else: sys.exit(__doc__)
