#!/usr/bin/env python3
"""audience v1 — l'échéancier public des prédictions. Né le 24/08/2026.

CRITÈRES PRÉ-ENREGISTRÉS DE V1 (gelés par registre.py) :
  - v1 réussit si : trois affaires réelles sont inscrites, inaltérables (hash), datées,
    chacune avec son juge (jeu de données futur) et son arbitre (script d'attaque à geler).
  - Le tribunal NE SIÈGE PAS avant l'arrivée du juge : `verdict` refuse sans données.
  - Tout acteur (humain ou IA) a un casier public : validées / réfutées / en attente.
Usage : audience.py inscrire aff.json | role | verdict <id>
"""
import sys, json, hashlib, pathlib, datetime
R = pathlib.Path(__file__).resolve().parent / "audience.json"
def _l(): return json.loads(R.read_text(encoding="utf-8")) if R.exists() else {"affaires":{}, "acteurs":{}}
def inscrire(p):
    d=_l(); a=json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    if a["id"] in d["affaires"]:
        sys.exit(f"[audience] {a['id']} déjà au rôle ({d['affaires'][a['id']]['hash']}) — pas de double inscription.")
    a["inscrite_le"]=datetime.date.today().isoformat()
    a["hash"]=hashlib.sha256(json.dumps(a,sort_keys=True).encode()).hexdigest()[:12]
    d["affaires"][a["id"]]=a
    for act in a["acteurs"]:
        c2=d["acteurs"].setdefault(act,{"validees":0,"refutees":0,"en_attente":0}); c2["en_attente"]+=1
    R.write_text(json.dumps(d,indent=1,ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"[audience] inscrite : {a['id']}  ({a['hash']})  juge attendu : {a['juge']}")
def role():
    d=_l()
    print("RÔLE D'AUDIENCE"); 
    for i,a in d["affaires"].items():
        print(f"  {i} | {a['affirmation'][:64]} | juge: {a['juge']} | échéance ~{a['echeance']} | {a['hash']}")
    print("CASIERS:", json.dumps(d["acteurs"],ensure_ascii=False))
def verdict(i):
    sys.exit(f"[audience] {i}: le juge n'est pas arrivé — le tribunal ne siège pas sur des intentions.")
if __name__=="__main__":
    c=sys.argv[1:] or ["?"]
    {"inscrire":lambda:inscrire(c[1]),"role":role,"verdict":lambda:verdict(c[1])}.get(c[0],lambda:sys.exit(__doc__))()
