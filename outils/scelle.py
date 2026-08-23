#!/usr/bin/env python3
"""scellé v1 — l'arbitre de l'affaire DR3-beta, construit AVANT l'arrivée du juge (24/08/2026).

PROTOCOLE SOUS SCELLÉS (rien ici ne sera modifié après publication du hash) :
  DONNÉES ATTENDUES : DESI DR3, format DR2 (points BAO DM/rd, DH/rd, DV/rd + covariances),
    combinées à Pantheon+ et aux distance-priors Planck exactement comme dans test_wE_v3.py
    (gelé). Tout changement de format sera traité par adaptateur SANS toucher aux seuils,
    l'adaptateur étant lui-même gelé avant lecture des données.
  VERDICTS (exhaustifs, exclusifs) :
    - VALIDÉE  si beta(DR3) ∈ [2,42 ; 2,60] à 1σ ET |kappa| < 0,24 maintenu.
    - RÉFUTÉE  si beta(DR3) exclut [2,42 ; 2,60] à >3σ, OU si w=-beta/(3Ht) perd contre
      LCDM de dAIC > +6, OU si beta1 mesuré exclut +0,06±0,31 à >3σ.
    - INDÉCISE sinon — et INDÉCISE n'est pas VALIDÉE.
  RÈGLE : aucun verdict sans données. Aucun seuil modifiable après scellement.
Usage : scelle.py sceau | verdict <donnees_dr3>
"""
import sys, hashlib, pathlib, json, datetime
def sceau():
    h=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    print(f"SCELLÉ le {datetime.date.today()} — à publier tel quel (dépôt, réseaux, papier A) :")
    print(f"  sha256(scelle.py) = {h}")
    lock=json.loads(pathlib.Path('registre.lock').read_text()) if pathlib.Path('registre.lock').exists() else {}
    if 'test_wE_v3.py' in lock: print(f"  pipeline gelé     = {lock['test_wE_v3.py']['sha256'][:16]}…")
    print("  Quiconque compare ce hash au fichier en 2027 vérifie que l'analyse n'a pas bougé.")
def verdict(p):
    if not pathlib.Path(p).exists():
        sys.exit(f"[scellé] {p} introuvable : le juge n'est pas arrivé. L'enveloppe reste fermée.")
    print("[scellé] données présentes — exécution du protocole gelé (v2 : appel test_wE_v3).")
if __name__=="__main__":
    a=sys.argv[1:]
    {"sceau":sceau,"verdict":lambda:verdict(a[1])}.get(a[0] if a else "?",lambda:sys.exit(__doc__))()
