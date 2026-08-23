#!/usr/bin/env python3
"""k-tracker v1 — posterieur vivant du couplage cosmologique des trous noirs (M ∝ a^k).

CRITÈRES PRÉ-ENREGISTRÉS (gelés par registre.py) :
  - v1 réussit si : il ingère un fichier de contraintes, REFUSE de combiner toute entrée
    non vérifiée contre sa source primaire, et publie l'état (vérifiées / à vérifier).
  - v1 échoue si : un postérieur est émis à partir d'une entrée statut != "verifie".
  - Chaque passage au statut "verifie" exige : citation exacte + valeur + qui a relu + date.
Usage : ktracker.py etat contraintes_k.json | combiner contraintes_k.json
"""
import sys, json, pathlib, datetime
def _l(p): return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
def etat(p):
    d=_l(p); print(f"ÉTAT k-tracker — {datetime.date.today()}")
    for c in d["contraintes"]:
        print(f"  [{c['statut']:>10}] {c['id']:<12} {c['source']:<28} {c.get('borne','(valeur à relire)')}")
    v=[c for c in d["contraintes"] if c["statut"]=="verifie"]
    print(f"  -> {len(v)} vérifiée(s) / {len(d['contraintes'])} ; combinables : {len(v)}")
def combiner(p):
    d=_l(p); v=[c for c in d["contraintes"] if c["statut"]=="verifie"]
    if not v: sys.exit("[k-tracker] REFUS : 0 contrainte vérifiée — aucun postérieur n'est émis "
                       "sur des valeurs non relues. Relire les sources primaires d'abord.")
    print("[k-tracker] combinaison de", len(v), "contraintes (v2 : vraisemblance produit)")
if __name__=="__main__":
    a=sys.argv[1:]; 
    {"etat":lambda:etat(a[1]),"combiner":lambda:combiner(a[1])}.get(a[0] if a else "?",lambda:sys.exit(__doc__))()
